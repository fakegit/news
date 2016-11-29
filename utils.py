#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"
from news.models import Settings 
""" 
 util tools
""" 
#---------- code begins below -------

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