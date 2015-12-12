#-*-encoding:utf-8-*-

from django import template
from news.getqiu.statistics.hotwords import HotWords
register = template.Library()

@register.inclusion_tag('news/hot_words_list.part.html',name='hotwords')
def hotwords():
	words_list = HotWords.read_most()
	return {'hotwords':words_list}
	#return {'hotwords':['中国','美国']}
	