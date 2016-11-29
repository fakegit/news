#-*-encoding:utf-8-*-

from django import template
from news.getqiu.statistics.hotwords import HotWords
from django.core.cache import cache
from news.models import Settings
from news.utils import getDBConfigure
register = template.Library()

@register.inclusion_tag('news/hot_words_list.part.html',name='hotwords')
def hotwords():
    #words_list = HotWords.read_most()
    if not cache.get("hot_words_list"):
        ##
        # get setting from db
        # RECOMM_CACHE_LIFE = 30
        ##
        
        RECOMM_CACHE_LIFE = getDBConfigure("RECOMM_CACHE_LIFE",default="30",type_=int)

        hot_words_list = HotWords.appear_most()
        cache.set("hot_words_list",hot_words_list,RECOMM_CACHE_LIFE)       
    return {'hotwords':cache.get("hot_words_list")}
    #return {'hotwords':['中国','美国']}
    