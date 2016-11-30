#-*-coding:utf-8-*-
from datetime import date,timedelta 
from news.getqiu.search.context import ViewContext
from news.models import Category

def datefilter(queryset,start_time=None,end_time=date.today()):
    """
    这个函数需要一个queryset和起始和结束的日期
    返回一个经过筛选的queryset
    这个filter是针对news的，因为数据待筛选的字段必须确定
    """
    #today = date.today()
    #start_time = end_time-timedelta(days=delta_days)
    return queryset.filter(news_time__gte=start_time,news_time__lte=end_time)
    
    
def categoryfilter(queryset,category):
    if category == 'all':
        return queryset
    else:
        #return queryset.filter(category__category=category)
        return queryset.filter(section=category)
        
        
class NewsFilter():
    
    def __init__(self,category,start_time,end_time=date.today()):
        #self.queryset = queryset
        self.category = category
        self.start_time = start_time
        self.end_time = end_time
        
    def execute(self,view_context):
        categorized_queryset = categoryfilter(view_context.queryset,self.category)
        date_filtered_queryset = datefilter(categorized_queryset,self.start_time,self.end_time)
        filtered_context = {'filter_info':{
                    'category_filter':Category.objects.all(),
                    'active_category_filter':self.category,
                }
        }
        
        url_parameter_dict = {'category':self.category,
                              "start_time":self.start_time,
                              "end_time":self.end_time
                              }
        
        current_view_context =  ViewContext(date_filtered_queryset,filtered_context,url_parameter_dict)
        return current_view_context.merge(view_context)
        
        
