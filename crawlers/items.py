# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy_djangoitem import DjangoItem
from news.models import *
#from wooyun.models import HoleModel,HoleUpdator


class CrawlersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    

    
class NewsItem(scrapy.Item):
    
    title=scrapy.Field()
    rank=scrapy.Field()
    news_time=scrapy.Field()
    publisher=scrapy.Field()
    news_url=scrapy.Field()
    content=scrapy.Field()
    hash_digest = scrapy.Field()
    site = scrapy.Field()
    category = scrapy.Field()


#class HoleItem(DjangoItem):
#    django_model = HoleModel

#class HoleUpdatorItem(DjangoItem):
#    django_model = HoleUpdator
