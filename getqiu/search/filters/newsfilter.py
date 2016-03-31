#-*-coding:utf-8-*-
from datetime import date,timedelta 
from news.getqiu.search.context import ViewContext
from news.models import Category

def datefilter(queryset,delta_days,end_time=date.today()):
    """
    这个函数需要一个queryset和起始和结束的日期
    返回一个经过筛选的queryset
    这个filter是针对news的，因为数据待筛选的字段必须确定
    """
    #today = date.today()
    start_time = end_time-timedelta(days=delta_days)
    return queryset.filter(news_time__gt=start_time).filter(news_time__lte=end_time)
    
    
def categoryfilter(queryset,category):
    if category == 'all':
        return queryset
    else:
        return queryset.filter(category__category=category)
        
        
class NewsFilter():
    
    def __init__(self,category,delta_days,end_time=date.today()):
        #self.queryset = queryset
        self.category = category
        self.delta_days = delta_days
        self.end_time = end_time
        
    def execute(self,view_context):
        categorized_queryset = categoryfilter(view_context.queryset,self.category)
        date_filtered_queryset = datefilter(categorized_queryset,self.delta_days,self.end_time)
        filtered_context = {'filter_info':{'time_filter':[
            {'value':1,'tag':'一天内'},
            {'value':7,'tag':'一周内'},
            {'value':30,'tag':'一月内'},
            {'value':365,'tag':'一年内'},
            {'value':3650,'tag':'所有'},                                    
        ],'active_time_filter':self.delta_days,
            'category_filter':Category.objects.all(),
            #[
            #    {'value':'finacial','tag':'经济'},
            #    {'value':'Headline','tag':'头条类'},
            #    {'value':'technology','tag':'科技类'},
            #    {'value':'mobile','tag':'手机类'},
            #    {'value':'all','tag':'所有'},
            #],
            'active_category_filter':self.category,
                }
        }
        
        url_parameter_dict = {'category':self.category,'delta_days':self.delta_days}
        
        current_view_context =  ViewContext(date_filtered_queryset,filtered_context,url_parameter_dict)
        return current_view_context.merge(view_context)
        
        
