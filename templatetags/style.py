#-*-encoding:utf-8-*-

from django import  template 
from django.template.defaultfilters import safe
from news.settings import RANK_SORT_PARAMETER
register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addplaceholder')
def addplaceholder(value,arg):
	return value.as_widget(attrs={'placeholder':"%d条新闻供您检索"%arg})

@register.filter(name="adjustrank")
def adjustrank(value):
	return RANK_SORT_PARAMETER-value