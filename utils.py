#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

import datetime
import six
from six import iteritems
import hashlib
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


def utf8(string):
    """
    Make sure string is utf8 encoded bytes.

    If parameter is a object, object.__str__ will been called before encode as bytes
    """
    if isinstance(string, six.text_type):
        return string.encode('utf8')
    elif isinstance(string, six.binary_type):
        return string
    else:
        return six.text_type(string).encode('utf8')

md5 = lambda x: hashlib.md5(utf8(x)).hexdigest()


def time2str(time_):
    return time_.strftime("%Y-%m-%d")