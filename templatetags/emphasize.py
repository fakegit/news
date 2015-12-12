#-*-encoding:utf-8-*-

from django import  template 
from django.template.defaultfilters import safe
from news.models import News
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
	return News.objects.all().count()
	#return "192929"
	