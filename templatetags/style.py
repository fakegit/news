#-*-encoding:utf-8-*-

from django import  template 
from django.template.defaultfilters import safe
register = template.Library()

@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})
