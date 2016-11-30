#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 news module configure
""" 
#---------- code begins below -------
from news.utils import getDBConfigure
from django.core.cache import cache

def getDaysRangeForSearchResult():
    if not cache.get("DaysRangeForSearchResult"):
        DaysRangeForSearchResult = getDBConfigure("DAYS_RANGE_FOR_SEARCH_RESULT",30,type_=int)
        DaysRangeCacheLife = getDBConfigure("DAYS_RANGE_CACHE_LIFE",24*60*60,type_=int)
        cache.set("DaysRangeForSearchResult",DaysRangeForSearchResult,DaysRangeCacheLife)
    return cache.get("DaysRangeForSearchResult")