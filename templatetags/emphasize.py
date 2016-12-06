#-*-encoding:utf-8-*-

from django import  template 
from django.template.defaultfilters import safe
from news.models import News
import lxml.html
from django.core.cache import cache
from news.configure import getDBConfigure
from pywebsites import settings

register = template.Library()

def addredtag(initial_string,one_word):
    """
        在给定的字符串中，将某些关键词着重处理
    """
    return initial_string.replace(one_word,"<font color='red'>"+one_word+"</font>")

@register.filter(name='redkeywords')
def redkeywords(input_string,keywords_list):
    """
     对input_string当中的keywords做着重处理
    """
    taged_sring = reduce(addredtag,keywords_list,input_string)
    return safe(taged_sring)
    
    
@register.assignment_tag(name="newsvolume")
def newsvolume():
    """
        得到总数，并且缓存指定时间
    """
    if not cache.get("news_amount"):
        #print "not using cache"
        news_amount = News.objects.all().count()
        newsVolumeCountCacheLife = getDBConfigure("NEWS_COUNT_CACHE_LIFE",default=4*60*40,type_=int)
        cache.set('news_amount',news_amount, newsVolumeCountCacheLife)  
    return cache.get("news_amount")
    #return "192929"
    
@register.filter(name="find_cover_img")
def find_cover_img(input_string):
    """
        在content当中查找一张图片
    """
    DEFAULT_NEWS_COVER = "/static/news/image/newsCover.jpg"
    if not input_string:
        #有些时候，只获取到标题，没有新闻body,不判断要躺枪..
        return DEFAULT_NEWS_COVER
    dom = lxml.html.document_fromstring(input_string)
    covers = dom.xpath("//img/@src[starts-with(.,'http')]")
    news_cover = covers[0] if covers else DEFAULT_NEWS_COVER
    return news_cover

@register.filter(name="cdnadapter")
def cdnadapter(originsource):
    """
        替换相关的图片
    """
    static_url = settings.STATIC_URL
    if static_url.startswith("/static/"):
        #说明配置就是 /static 不用修改
        return originsource
    elif static_url.startswith("http"):
        # 启动了cdn
        if originsource.startswith("/static/"):
            # 将/static 替换成 cdn
            return originsource.replace("/static/",static_url)
    return originsource