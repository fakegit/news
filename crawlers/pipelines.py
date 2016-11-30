# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem,CloseSpider
from news.models import *
import logging
import re
import datetime
#from datetime.date import today
from hashlib import md5
from news.getqiu.search.createtag import AddTag
import lxml.html

class NewsPipeline(object):
    
    def find_cover_img(self,input_string):
        DEFAULT_NEWS_COVER = "/static/news/image/newsCover.jpg"
        if not input_string:
            #有些时候，只获取到标题，没有新闻body,不判断要躺枪..
            return DEFAULT_NEWS_COVER
        dom = lxml.html.document_fromstring(input_string)
        covers = dom.xpath("//img/@src[starts-with(.,'http')]")
        news_cover = covers[0] if covers else DEFAULT_NEWS_COVER
        return news_cover

    def process_item(self,item,spider):
        try:
            try:

            #item['hash_digest'] = md5(item['title'].encode('utf-8')+item.get('news_time',str(datetime.date.today())).encode('utf-8')).hexdigest()
                item['hash_digest'] = md5(item['title'].encode('utf-8')+item['news_time'].encode('utf-8')).hexdigest()
            except KeyError:
                raise DropItem("give up this news")
                
            try:
                exist_news = News.objects.only('id','title').get(hash_digest=item['hash_digest'])
                #tag_adder=AddTag(exist_news,'title')
                #tag_adder.save()#老新闻还是检查一边，虽然没必要                
                logging.info("the news  %s is in the category(%s)"%(item['title'],item['category']))
            except News.DoesNotExist:
                #category 字段是在页面内容提取当中出现，不存放在news表中，故pop
                news_category = item.pop("category")
                news_cover = self.find_cover_img(item['content'])
                #字典拆分，直接填入；但是扩展性不好
                newItem = News(cover=news_cover,section=news_category,**dict(item))
                #newItem.cover = news_cover
                #save()存入数据库，newItem也就有了id
                newItem.save()
                try:
                    #用try的原因是：如果用if 每次都需要判断，分类很少不存在，try
                    #做的动作相对更少
                    category_object = Category.objects.get(category=news_category)
                    category_object.news.add(newItem)
                except Category.DoesNotExist:
                    #分类不存在的情况下
                    category_object = Category(category=news_category)
                    category_object.save()
                    category_object.news.add(newItem)
                #这个动作完了后，可以加入拆词功能
                
                tag_adder=AddTag(newItem,'title')
                tag_adder.save()#完成添加tag功能
                    
                    
                
                logging.info("saved the news %s in %s <<<<"%(item['title'],news_category))
                
                
            except News.MultipleObjectsReturned:
                logging.warning("MultipleObjectsReturned,delete the duplications>>>")
                News.objects.filter(news_url=item['title']).delete()
                
        except Exception,e:
            logging.warning("error accoured on %s;skipped"%item['news_url'])
            raise e
            
            
            
    
    