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
    """
        默认搜索时间范围(最近30天)
    """
    if not cache.get("DaysRangeForSearchResult"):
        DaysRangeForSearchResult = getDBConfigure("DAYS_RANGE_FOR_SEARCH_RESULT",30,type_=int)
        DaysRangeCacheLife = getDBConfigure("DAYS_RANGE_CACHE_LIFE",24*60*60,type_=int)
        cache.set("DaysRangeForSearchResult",DaysRangeForSearchResult,DaysRangeCacheLife)
    return cache.get("DaysRangeForSearchResult")

def getMaxCountForSearchResult():
    """
        默认搜索结果最大条目数
    """
    if not cache.get("MaxCountForSearchResult"):
        MaxCountForSearchResult = getDBConfigure("SEARCH_RESULT_MAX_COUNT",200,type_=int)
        MaxResultCountCacheLife = getDBConfigure("MAX_RESULT_COUNT_CACHE_LIFE",24*60*60,type_=int)
        cache.set("MaxCountForSearchResult",MaxCountForSearchResult,MaxResultCountCacheLife)
    return cache.get("MaxCountForSearchResult")


def getSearchTrace():
    """
        是否开启搜索跟踪
    """
    if not cache.get("SearchTrace"):
        SearchTrace = getDBConfigure("SEARCH_TRACE",default="1",type_=lambda x:bool(int(x)))
        MaxSearchTraceCacheLife = getDBConfigure("SEARCH_TRACE_CACHE_LIFE",60,type_=int)
        cache.set("SearchTrace",SearchTrace,MaxSearchTraceCacheLife)
    return cache.get("SearchTrace")

def banSpider():
    """
        是否反爬虫
    """
    if not cache.get("BanSpider"):
        BanSpider = getDBConfigure("BAN_SPIDER",default="0",type_=lambda x:bool(int(x)))
        MaxBanSpiderCacheLife = getDBConfigure("BAN_SPIDER_CACHE_LIFE",60,type_=int)
        cache.set("BanSpider",BanSpider,MaxBanSpiderCacheLife)
    return cache.get("BanSpider")

def getMaxSearchPerDay():
    """
        设置每天最多搜索次数
    """
    if not cache.get("MaxSearchPerDay"):
        MaxSearchPerDay = getDBConfigure("MAX_SEARCH_PER_DAY",default=399,type_=int)
        MaxMaxSearchPerDayCacheLife = getDBConfigure("MAX_SEARCH_PER_DAY_CACHE_LIFE",60,type_=int)
        cache.set("MaxSearchPerDay",MaxSearchPerDay,MaxMaxSearchPerDayCacheLife)
    return cache.get("MaxSearchPerDay")