#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

import datetime
""" 
 util tools
""" 
#---------- code begins below -------




def convert2date(dtstr):
    """
        将字符串时间转化为对象
    """
    if isinstance(dtstr,datetime.date):
        return dtstr
    if isinstance(dtstr,datetime.datetime):
        return dtstr.date()    
    return datetime.datetime.strptime(dtstr, "%Y-%m-%d").date()