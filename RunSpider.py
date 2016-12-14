#!/usr/bin/python
#-encoding:utf-8-
from __future__ import with_statement
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import os
import sys
import ConfigParser


def getConfiguredProcess():
    """
        配置程序环境
    """
    current_path = os.path.dirname(os.path.abspath(__file__))
    #add current_path to python path if no in the python path
    if current_path not in sys.path:
        sys.path.append(current_path)

    
    #find the scrapy.cfg file
    config_file = os.path.join(current_path,'scrapy.cfg')
    
    #get a configureParser
    config_parser=ConfigParser.ConfigParser()
    
    #the purpose of open scrapy.cfg is to set the environment path of SCRAPY_SETTINGS_MODULE
    with open(config_file,'r') as configures:
        config_parser.readfp(configures)
        settings_module= config_parser.get('settings','default')
        os.environ['SCRAPY_SETTINGS_MODULE'] = settings_module  
    #以后要自动运行的spider可以直接在cfg文件当中直接添加      
    process = CrawlerProcess(get_project_settings())

    return process 

def crawl():
    """
        开启爬虫
    """
    spiderList = ["news_qq","mil_qq","sports_qq","ent_qq","finance_qq",
                  "stock_qq","auto_qq","tech_qq","digi_tech_qq","cd_house_qq",
                  "bj_house_qq","edu_qq",
                  "money_163","tech_163","news_163","sports_163","ent_163",
                  "auto_163","home_163","discovery_163","mobile_163",
                  "digi_163","lady_163","edu_163","jiankang_163","travel_163","house_163"]
    process = getConfiguredProcess()

    #spider = spiderList[getNext(len(spiderList))]
    process.crawl("qq")
    process.crawl("163")
    #runAllSpider(process,spiderList)
    
    process.start()
    #print "the running spider is %s" % spider

def getNext(queueSize):
    """
        获取下一个
    """
    from news.models import Runtime
    nextTurn = Runtime.getOption("NEXT_INDEX_OF_SPIDER",default=0,type_=int,comment="下一轮运行的编号")
    Runtime.setOption("NEXT_INDEX_OF_SPIDER",(nextTurn+1)%queueSize)
    return nextTurn

def runAllSpider(process,spiderList):
    """
    """
    map(lambda s:process.crawl(s),spiderList)

if __name__ == "__main__":
    crawl()