#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"
from news.models import News
from news.configure import getMaxCountForSearchResult as maxcount
""" 
 排序策略
""" 
#---------- code begins below -------
class OrderStretagy(object):
    
    def limitResultCount(self,queryset):
        return queryset[0:maxcount()]
        

class NormalOrder(OrderStretagy):
    
    def __init__(self,queryset):
        self.queryset = self.limitResultCount(queryset.order_by("-news_time","-rank"))
        self.__idList = None

    def __getIdList(self):
        if self.__idList == None:
            self.__idList =  [x[0] for x in self.queryset.values_list("id")]
        return self.__idList

    @property
    def count(self):
        """
            return the count
        """        
        return len(self.__getIdList())

    @property
    def result(self):
        """
            return the queryset
        """
        return self.queryset

class InQueryBasedOrder(OrderStretagy):
    """
        采用in查询来做排序
    """
    def __init__(self,queryset):
        self.queryset = self.limitResultCount(queryset)
        self.__idList = None

    def __getIdList(self):
        if self.__idList == None:
            self.__idList =  [x[0] for x in self.queryset.values_list("id")]
        return self.__idList

    @property
    def count(self):
        """
            return the count
        """
        return len(self.__getIdList())

    @property
    def result(self):
        """
            return the queryset
        """
        return News.objects.filter(id__in=self.__getIdList()).order_by("-id","-news_time","-rank")