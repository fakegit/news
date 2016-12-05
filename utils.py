#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

import datetime
import six
from six import iteritems
import hashlib
from news.models import Vocabulary
import os
from os.path import dirname
from news.configure import getDBConfigure,setDBConfigure
import logging 

logger = logging.getLogger(__name__)
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

def build_user_dict():
    """
        创建新的用户自定义词典
    """
    DIR = dirname(os.path.abspath(__file__))
    userDictFile = os.path.join(DIR,"userdict.txt")

    useUserDefinedDict = getDBConfigure("USE_USER_DEFINED_DICT",default=0,type_=lambda x:bool(int(x)))
    if not useUserDefinedDict:
        nullUserDictFile = os.path.join(DIR,"nulluserdict.txt")
        if not os.path.exists(nullUserDictFile):
            with open(nullUserDictFile,"w+") as f:
                print "created nulluserdict.txt"
        print "USE_USER_DEFINED_DICT=OFF,use null dict instead"
        return nullUserDictFile

    needRebuildUserDefinedDict = getDBConfigure("RE_BUILD_USER_DEFINED_DICT",default=1,type_=lambda x:bool(int(x)))
    if not needRebuildUserDefinedDict:
        if not os.path.exists(userDictFile):
            with open(userDictFile,"w+") as f:
                print "File userdict.txt does not exist,create an empty one"
        print "use the old userdict.txt file"
        return userDictFile

    ##
    # 需要重新制作字典
    ##    
    setDBConfigure("RE_BUILD_USER_DEFINED_DICT",option=0) # 不用再重新制作字典了，重置标志位   
    if os.path.exists(userDictFile):
        os.remove(userDictFile)
    
    template_line = u"{word} {frequency} {characteristic}\n"
    with open(userDictFile,'w') as f:
        wordCount = Vocabulary.objects.filter(brand="user").count()
        step = 300
        writted = 0
        while writted < wordCount:
             
            words = Vocabulary.objects.filter(brand="user")\
                              .values("word","frequency","characteristic")\
                              .all()[writted:writted+step]
            
            for word in words:
                f.write(template_line.format(**word).encode("utf-8"))

            writted  = writted + step
    print "rebuilt the userdict.txt"
    return userDictFile
        