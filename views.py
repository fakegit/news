#-*-coding:utf-8-*-
import urllib
import random
import datetime
import time
from datetime import timedelta

import jieba
from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse
from django.db.models import Count,Avg,Sum,F,Q
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required

from news.forms import SearchBoxForm,SuggestionForm,TestForm,TimeWindowForm,MigrateRelationForm
from news.models import News,SearchTrace,Tags,TagsNews
from news.getqiu.search.filters.newsfilter  import NewsFilter
from news.getqiu.search.filters.paginator import PageFilter
from news.getqiu.search.context import ViewContext    
from news.getqiu.statistics.count import ClickRecoder
from news.getqiu.search.engine import TagBasedSearch
from news.getqiu.search import  conf

from news.configure import getDaysRangeForSearchResult as daysrange
from news.configure import getSearchTrace,banSpider,getMaxSearchPerDay
from news.configure import getHalfRankForTrend
from news.configure import getMaxItemOnHeadline
from news.utils import convert2date,time2str,md5
from news.settings import MAX_RECOMMEDED_NEWS_ON_SEARCH_PAGE


from ip2location.ipresolver import Resolver
from ip2location.recoder import VisitorRecoder
from ip2location.generator import IpGenerator
from ip2location.userdetail import RequestInfo

class FloatSum(Sum):
    function="SUM"
    name = "FloatSum"

    def convert_value(self, value, expression, connection, context):
        if value is None:
            return 0
        return float(value)    

class LoginRequiredMixin(object):
    
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view,login_url="/")

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
            start_view_context = ViewContext(News.objects.only('title','hash_digest','news_time','rank','cover',"news_url").all(),
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

class WordTrendAPI(TemplateView):
    """
        词语趋势分析源数据
    """
    def get(self,request):
        query_word = request.GET.get('q',"韩国")
        start_time = request.GET.get("start",datetime.date.today()-timedelta(days=daysrange()))
        end_time = request.GET.get("end",datetime.date.today())  

        start_time = convert2date(start_time) if start_time else datetime.date.today()-timedelta(days=daysrange())
        end_time = convert2date(end_time) if end_time else datetime.date.today()              
        halfrank = getHalfRankForTrend()
        word_trend = News.objects\
                         .filter(news_time__gte=start_time,news_time__lte=end_time)\
                         .filter(tags__tag=query_word)\
                         .order_by("news_time")\
                         .values("news_time")\
                         .annotate(n=Count("news_time"))\
                         .annotate(s=FloatSum(halfrank/(999-F("rank")+halfrank)))
        # 整理数据，做插零处理
        word_trend = self.contiue_date(word_trend,start_time,end_time)
        word_trend = [{"time":time2str(d["news_time"]),"count":d["n"],"score":d["s"],"weight":d["w"]} for d in word_trend]
        return JsonResponse(word_trend,safe=False)

    def contiue_date(self,word_trend,start,end):
        """
            通过group by得到的时间是不连续的，应该通过插入0让它连续
        """
        new_word_trend_list = []
        tmp = start
        origin_index = 0
        while tmp <= end:
            if origin_index >= len(word_trend):
                nextDataCeil = {"news_time":tmp,"n":0,"s":0,"w":0}
                #new_word_trend_list.append(nextDataCeil)
                tmp = tmp + timedelta(days=1)                
            elif tmp != word_trend[origin_index]["news_time"]:
                # 只要是不等于，都应该插入0，不管是大还是小
                nextDataCeil = {"news_time":tmp,"n":0,"s":0,"w":0}
                tmp = tmp + timedelta(days=1)
            elif tmp == word_trend[origin_index]["news_time"]:
                #new_word_trend_list.append(word_trend[origin_index])
                nextDataCeil = word_trend[origin_index]
                nextDataCeil["w"] = float(nextDataCeil["s"]/nextDataCeil["n"])
                tmp = tmp + timedelta(days=1)
                origin_index = origin_index + 1
            
            
            new_word_trend_list.append(nextDataCeil)

        return new_word_trend_list
            



class WordTrend(TemplateView):
    """
        词语趋势展示图
    """
    template_name = "news/word_trend.html"
    def get(self,request):
        q = request.GET.get("q","中国")
        return render(request,self.template_name,context = {"q":q})

class NewsInToday(TemplateView):
    """
        provide with today's news
    """
    template_name = 'news/news_in_today.html'
    def get(self,request):
        """ """
        maxItemOnHeadline = getMaxItemOnHeadline()
        today = datetime.date.today()
        news_today = News.objects.only('title','news_time','rank','cover','content',"news_url")\
                                 .filter(news_time=today,rank__gte=997).order_by("-rank")[0:maxItemOnHeadline]
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

class MigrateRelation(LoginRequiredMixin,TemplateView):

    template_name = "news/migrate_relation.html"

    def get(self,request):
        """
        """
        migrate_relation_form = MigrateRelationForm()
        context = {"form":migrate_relation_form}
        return render(request,self.template_name,context)

    def post(self,request):
        """
         仅仅是将原来的关系复制了一份，原先的并不删除原先
        """
        migrate_relation_form = MigrateRelationForm(request.POST)
        if migrate_relation_form.is_valid():
            oldtag = migrate_relation_form.cleaned_data["oldtag"]
            newtag = migrate_relation_form.cleaned_data["newtag"]

            key_words = self.find_key_words(oldtag)
            oldnewsObject = reduce(self.narrow_queryset,key_words,News.objects.all())
            try:
                newTagObject = Tags.objects.get(tag=newtag)
            except Tags.DoesNotExist:
                newTagObject = Tags(tag=newtag,tag_hash=md5(newtag))
                newTagObject.save()

            TagsNews.objects.bulk_create([
                TagsNews(news=n,tags=newTagObject) for n in oldnewsObject if not TagsNews.objects.filter(news=n,tags=newTagObject).exists()
            ])

            return redirect(reverse('news:transform')+"?reason=%s" % "applied the adjustion")
        else:
            return render(request,self.template_name,context={"form":migrate_relation_form})

    def narrow_queryset(self,tmp_queryset,tag):
        return tmp_queryset.filter(tags__tag=tag)
        
    def find_key_words(self,input_sting):
        key_words = jieba.lcut(input_sting)
        #key_words = jieba.cut_for_search(input_sting)
        key_words = list(set(key_words))#去除重复
        key_words = filter(lambda x:False if x in conf.MEANINGLESS_WORDS else True,key_words)
        return key_words


class AppManager(LoginRequiredMixin,TemplateView):
    """
        词语趋势展示图
    """
    template_name = "news/app_manager.html"
    def get(self,request):
        return render(request,self.template_name,context = {})

class NewsAPI(TemplateView):

    def get(self,request,action):
        if hasattr(self,action):
            return getattr(self,action)(request)
        else:
            return JsonResponse({"status":""})

    def spotForOneDay(self,request):
        """
            返回一个List = [{"title":"XXX","hash_digest":"XXX"},.....]
        """
        q = request.GET.get("q","中国")
        time = request.GET.get("t",datetime.date.today())
        time = convert2date(time)
        topNews = News.objects.filter(news_time=time,tags__tag=q).values("title","hash_digest").order_by("-rank")[0:3]
        newsList = [t for t in topNews]
        return JsonResponse(newsList,safe=False)

    def countEveryDay(self,request):
        start_time = request.GET.get("start",datetime.date.today()-timedelta(days=daysrange()))
        end_time = request.GET.get("end",datetime.date.today())
        start_time = convert2date(start_time) if start_time else datetime.date.today()-timedelta(days=daysrange())
        end_time = convert2date(end_time) if end_time else datetime.date.today()  
        news_count = News.objects\
                         .filter(news_time__gte=start_time,news_time__lte=end_time)\
                         .order_by("news_time")\
                         .values("news_time")\
                         .annotate(n=Count("news_time"))
        # 整理数据，做插零处理
        news_count = self.contiue_date(news_count,start_time,end_time)
        news_count = [{"time":time2str(d["news_time"]),"count":d["n"]} for d in news_count]
        return JsonResponse(news_count,safe=False)

    def contiue_date(self,count,start,end):
        """
            通过group by得到的时间是不连续的，应该通过插入0让它连续
        """
        new_count_list = []
        tmp = start
        origin_index = 0
        while tmp <= end:
            if origin_index >= len(count):
                new_count_list.append({"news_time":tmp,"n":0})
                tmp = tmp + timedelta(days=1)                
            elif tmp != count[origin_index]["news_time"]:
                # 只要是不等于，都应该插入0，不管是大还是小
                new_count_list.append({"news_time":tmp,"n":0})
                tmp = tmp + timedelta(days=1)
            elif tmp == count[origin_index]["news_time"]:
                new_count_list.append(count[origin_index])
                tmp = tmp + timedelta(days=1)
                origin_index = origin_index + 1

        return new_count_list                  