#-*-encoding:utf-8-*-

from django import template
from news.getqiu.statistics.hotwords import HotWords
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('news/hot_words_list.part.html',name='hotwords')
def hotwords():
    #words_list = HotWords.read_most()
    if not cache.get("hot_words_list"):
        hot_words_list = HotWords.read_most()
        cache.set("hot_words_list",hot_words_list,6*60*60)       
    return {'hotwords':cache.get("hot_words_list")}
    #return {'hotwords':['中国','美国']}
    