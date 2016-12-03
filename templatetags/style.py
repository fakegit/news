#-*-encoding:utf-8-*-

from django import  template 
from django.template.defaultfilters import safe
from news.settings import RANK_SORT_PARAMETER
import re 

register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.filter(name='addplaceholder')
def addplaceholder(value,arg):
	return value.as_widget(attrs={'placeholder':"%d条新闻供您检索"%arg})

@register.filter(name="adjustrank")
def adjustrank(value):
	"""
		调整rank显示值
	"""
	return RANK_SORT_PARAMETER-value

@register.filter(name="urldomain")
def urldomain(value):
	"""
		根据url得到域名
	"""
	domainRegex = r"https?://(?P<domain>([a-z0-9\-]+\.)+(com|cn))"
	domain = re.search(domainRegex,value)
	if domain:
		return domain.group("domain")
	else:
		return "getqiu.com"

@register.filter(name="sec2millis")
def sec2millis(value,digit=3):
	"""
	 将秒转化为毫秒,并精确小数点位数
	"""
	return round(value*1000,int(digit))