#!/usr/bin/python
#-encoding:utf-8-
from __future__ import with_statement
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import os
import sys
import ConfigParser


if __name__ == "__main__":
    #get the current path
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
    process.crawl('163')
    process.crawl('qq')
    #process.crawl('news_163')
    #process.crawl('finace_163')
    #process.crawl('tech_163')
    #process.crawl('mobile_163')
    process.start()
