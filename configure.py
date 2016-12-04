#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 news module configure
""" 
#---------- code begins below -------
from django.core.cache import cache
from news.models import Settings

def getDBConfigure(key,default="0",type_=str):
    """
        get configured value from db.
    """
    try:
        setting = Settings.objects.get(key=key)
    except Settings.DoesNotExist:
        setting = Settings(key=key,option=str(default))
        setting.save()
    return type_(setting.option)

def setDBConfigure(key,option):
    """
        set configure value in db
    """
    try:
        setting = Settings.objects.get(key=key)
        setting.option = str(option)
        setting.save()
    except Settings.DoesNotExist:
        setting = Settings(key=key,option=str(option))
        setting.save()     

def durationOfSettings():
    """
        配置有效时间，过期之后才会读取新设置的值,最小的粒度为 60s
    """
    if not cache.get("DurationOfSettings"):
        DurationOfSettings = getDBConfigure("DURATION_OF_SETTINGS",60,type_=int)
        cache.set("DurationOfSettings",DurationOfSettings,60)
    return cache.get("DurationOfSettings")


def getDaysRangeForSearchResult():
    """
        默认搜索时间范围(最近30天)
    """
    if not cache.get("DaysRangeForSearchResult"):
        DaysRangeForSearchResult = getDBConfigure("DAYS_RANGE_FOR_SEARCH_RESULT",30,type_=int)
        DaysRangeCacheLife = durationOfSettings()
        cache.set("DaysRangeForSearchResult",DaysRangeForSearchResult,DaysRangeCacheLife)
    return cache.get("DaysRangeForSearchResult")

def getMaxCountForSearchResult():
    """
        默认搜索结果最大条目数
    """
    if not cache.get("MaxCountForSearchResult"):
        MaxCountForSearchResult = getDBConfigure("SEARCH_RESULT_MAX_COUNT",200,type_=int)
        MaxResultCountCacheLife = durationOfSettings()
        cache.set("MaxCountForSearchResult",MaxCountForSearchResult,MaxResultCountCacheLife)
    return cache.get("MaxCountForSearchResult")


def getSearchTrace():
    """
        是否开启搜索跟踪
    """
    if not cache.get("SearchTrace"):
        SearchTrace = getDBConfigure("SEARCH_TRACE",default="1",type_=lambda x:bool(int(x)))
        MaxSearchTraceCacheLife = durationOfSettings()
        cache.set("SearchTrace",SearchTrace,MaxSearchTraceCacheLife)
    return cache.get("SearchTrace")

def banSpider():
    """
        是否反爬虫
    """
    if not cache.get("BanSpider"):
        BanSpider = getDBConfigure("BAN_SPIDER",default="0",type_=lambda x:bool(int(x)))
        MaxBanSpiderCacheLife = durationOfSettings()
        cache.set("BanSpider",BanSpider,MaxBanSpiderCacheLife)
    return cache.get("BanSpider")

def getMaxSearchPerDay():
    """
        设置每天最多搜索次数
    """
    if not cache.get("MaxSearchPerDay"):
        MaxSearchPerDay = getDBConfigure("MAX_SEARCH_PER_DAY",default=399,type_=int)
        MaxMaxSearchPerDayCacheLife = durationOfSettings()
        cache.set("MaxSearchPerDay",MaxSearchPerDay,MaxMaxSearchPerDayCacheLife)
    return cache.get("MaxSearchPerDay")