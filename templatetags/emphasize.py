#-*-encoding:utf-8-*-

from django import  template 
from django.template.defaultfilters import safe
from news.models import News
import lxml.html
from django.core.cache import cache
register = template.Library()

def addredtag(initial_string,one_word):
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
    if not cache.get("news_amount"):
        #print "not using cache"
        news_amount = News.objects.all().count()
        cache.set('news_amount',news_amount, 6*60*60)      
    return cache.get("news_amount")
    #return "192929"
    
@register.filter(name="find_cover_img")
def find_cover_img(input_string):
    DEFAULT_NEWS_COVER = "/static/news/image/newsCover.jpg"
    dom = lxml.html.document_fromstring(input_string)
    covers = dom.xpath("//img/@src[starts-with(.,'http')]")
    news_cover = covers[0] if covers else DEFAULT_NEWS_COVER
    return news_cover