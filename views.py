#-*-coding:utf-8-*-
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
# Create your views here.
from django.core.urlresolvers import reverse
from .forms import SearchBoxForm,SuggestionForm,TestForm,TimeWindowForm
from .models import News,SearchTrace
from news.getqiu.search.engine import TitleBasedEngine,TagBasedSearch
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import urllib
import random
import datetime
from datetime import timedelta
import time
from news.getqiu.search.filters.newsfilter  import NewsFilter
from news.getqiu.search.filters.paginator import PageFilter
#from django.http import QueryDict
from news.getqiu.search.context import ViewContext    
#from ip2location.models import Visitors,Ip2Location
from ip2location.ipresolver import Resolver
from ip2location.recoder import VisitorRecoder
from ip2location.generator import IpGenerator
from news.getqiu.statistics.count import ClickRecoder
from ip2location.userdetail import RequestInfo
#from django.db import connections
from news.configure import getDaysRangeForSearchResult as daysrange
from news.configure import getSearchTrace,banSpider,getMaxSearchPerDay
from news.utils import convert2date
from news.settings import MAX_RECOMMEDED_NEWS_ON_SEARCH_PAGE

class HomePage(TemplateView):
    template_name = 'news/home_page.html'

    def get(self,request):

        #ip_generator = IpGenerator() #ip地址本来应该从request当中获取，这里随机模拟一个
        visitor_recoder = VisitorRecoder()#实列化一个用户访问记录器
        request_info = RequestInfo(request)
        ip_info = visitor_recoder.save(request_info.ip,request_info.port)#记录用户
        #调试阶段，所以可以看看随机产生的ip，实际上线根据情况渲染    
        #connections['default'].queries    
        #search_form = SearchBoxForm()

        ##
        #   show the headline of today
        ##
        today = datetime.date.today()
        news_today = News.objects.only('title','hash_digest')\
                                 .filter(news_time=today,rank__gte=999)[0:MAX_RECOMMEDED_NEWS_ON_SEARCH_PAGE]

        context = {'ip_info':ip_info.values(),"search_form":SearchBoxForm(),"news_today":news_today}

        return render(request,self.template_name,context)
        
        
        
class SearchResult(TemplateView):
    template_name = 'news/searchResult.html'
    
    def get(self,request):
        """
         搜索提交是post还是get好呢？显然是get，因为不会有post的提示
        """
        search_form = SearchBoxForm(request.GET)
        if search_form.is_valid():
            #pass
            #这里应该添加实际的业务查询逻辑

            ##
            # request_info = RequestInfo(request)
            ##
            request_info = RequestInfo(request)

            if banSpider():
                if SearchTrace.getSearchTimeToday(request_info.ip) > getMaxSearchPerDay():
                    return redirect(reverse('news:transform')+"?reason=%s" % "the fucking evil spider please get away.")
            ######
            query_word = request.GET.get('search_word')
            category = request.GET.get('category','all')
            request_page = request.GET.get('page',1)

            start_time = request.GET.get("start_time",datetime.date.today()-timedelta(days=daysrange()))
            end_time = request.GET.get("end_time",datetime.date.today())

            start_time = convert2date(start_time) if start_time else datetime.date.today()-timedelta(days=daysrange())
            end_time = convert2date(end_time) if end_time else datetime.date.today()

            #以上获取筛选需要的字段
            start_view_context = ViewContext(News.objects.only('title','news_time','rank','cover',"news_url").all(),
                                             {'search_form':search_form,"news_start_date":start_time,"news_end_date":end_time},
                                             {})
            filter_list = [
                NewsFilter(category,start_time,end_time),
                TagBasedSearch(query_word),
                PageFilter(10,request_page),
                ]
            m = lambda context,_filter:_filter.execute(context) #这句话就是执行各个filter的接口
            start_search_clock  = time.time()
            view_context = reduce(m,filter_list,start_view_context)
            end_search_clock  = time.time()  
            #reduce 一把搞定！
            context = view_context.context
            context["search_elapsed_time"] = end_search_clock - start_search_clock


            ##
            #   处理记录逻辑
            ##
            if getSearchTrace():
                
                search_time_today = SearchTrace.getSearchTimeToday(request_info.ip)            
                trace = SearchTrace(expression=query_word,ip=request_info.ip)
                trace.save()
                context["search_time_today"] = search_time_today
            ######## END 记录逻辑  ###################

            return render(request,self.template_name,context)
            
        else:
            return redirect(reverse('news:home_page'))
    
    def post(self,request):
        search_form = SearchBoxForm(request.POST)
        if search_form.is_valid():
            #pass
            #这里应该添加实际的业务查询逻辑
            context = {'search_form':search_form}
            return render(request,self.template_name,context)
            
        else:
            return redirect(reverse('news:home_page'))
            
class NewsInToday(TemplateView):
    """
        provide with today's news
    """
    template_name = 'news/news_in_today.html'
    def get(self,request):
        """ """
        today = datetime.date.today()
        news_today = News.objects.only('title','news_time','rank','cover','content',"news_url")\
                                 .filter(news_time=today,rank__gte=997).order_by("-rank")
        context = {
            "news":news_today,
        }
        return render(request,self.template_name,context)
        

class DeleteSearchRecord(TemplateView):
    """
    """
    def get(self,request):
        """
        """
        SearchTrace.deleteOneDayAgo()
        #return render(request,self.template_name,context=None)
        return redirect(reverse('news:transform')+"?reason=%s" % "deleted outdated search record.")

class AddCrawlerTask(TemplateView):
    template_name = 'news/add_crawler_task.html'
    
    def get(self,request):
        context = {'name':'qiulimao'}
        return render(request,self.template_name,context)
        
        
class NewsDetail(TemplateView):
    template_name = "news/news_detail.html"
    context = {}
    
    def get(self,request,news_id):
        news_detail = News.objects.get(hash_digest=news_id)
        ClickRecoder.plus_one(news_detail)
        self.context = dict(self.context,**{'one_news':news_detail})
        return render(request,self.template_name,self.context)



class Suggestion(TemplateView):
    template_name='news/suggestion.html'
    
    def get(self,request):
        suggestion_form = SuggestionForm()
        context = {'form':suggestion_form}
        
        return render(request,self.template_name,context)
        
        
    def post(self,request):
        #new_suggestion = Suggestion(visitor='192.168.2.1')
        suggestion_form = SuggestionForm(request.POST)
        
        if suggestion_form.is_valid():
            request_info = RequestInfo(request)
            new_suggestion = suggestion_form.save(commit=False)
            new_suggestion.visitor = request_info.ip
            new_suggestion.save()
            context = {'form':suggestion_form}
            return redirect(reverse('news:transform')+"?reason=%s" % "recieved your suggestion")
        else:
            context = {'form':suggestion_form}
            return render(request,self.template_name,context)
            
            
class TransformPage(TemplateView):
    template_name = 'news/redirecting.html'
    
    def get(self,request):
        reason = request.GET.get("reason"," ")
        context = {"reason":reason}
        return render(request,self.template_name,context)        
        


class AboutUs(TemplateView):
    template_name = 'news/aboutus.html'
    
    def get(self,request):
        return render(request,self.template_name)