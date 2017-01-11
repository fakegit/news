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
from news.getqiu.search.createtag import AddTag
#import lxml.html
from news.utils import md5,utf8
import traceback

logger = logging.getLogger(__name__)



class NewsPipeline(object):
    
    # def find_cover_img(self,input_string):
    #     DEFAULT_NEWS_COVER = "/static/news/image/newsCover.jpg"
    #     if not input_string:
    #         #有些时候，只获取到标题，没有新闻body,不判断要躺枪..
    #         return DEFAULT_NEWS_COVER
    #     dom = lxml.html.document_fromstring(input_string)
    #     covers = dom.xpath("//img/@src[starts-with(.,'http')]")
    #     news_cover = covers[0] if covers else DEFAULT_NEWS_COVER
    #     return news_cover

    def process_item(self,item,spider):
        try:
            try:
                item['hash_digest'] = md5(item["title"]+item["news_time"])
                content = item["content"]
                #logger.info(u"the news cover is %s" % item["cover"])
            except KeyError:
                #raise DropItem("@@@@@ give up this news")
                logger.debug("@@@@ give up this item because of not enough infomation")
                raise DropItem("NotEnoughInfomation")
                
            try:
                exist_news = News.objects.only('id').get(hash_digest=item['hash_digest'])
                #tag_adder=AddTag(exist_news,'title')
                #tag_adder.save()#老新闻还是检查一边，虽然没必要                
                #logger.info("|||||| [%s] the news  %s"%(item['category'],item['title']))
            except News.DoesNotExist:
                #category 字段是在页面内容提取当中出现，不存放在news表中，故pop
                news_category = item.pop("category")
                #news_cover = self.find_cover_img(item['content'])
                #字典拆分，直接填入；但是扩展性不好
                newItem = News(section=news_category,**dict(item))
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
                    category_object = Category(category=news_category,category_name=news_category)
                    category_object.save()
                    category_object.news.add(newItem)
                #这个动作完了后，可以加入拆词功能
                
                tag_adder=AddTag(newItem,'title')
                tag_adder.save()#完成添加tag功能
                    
                logger.info("++++++ [%s] the news %s"%(news_category,item['title']))
                
                
            except News.MultipleObjectsReturned:
                logger.warning("-----MultipleObjectsReturned,delete the duplications")
                News.objects.filter(news_url=item['title']).delete()
     
        except Exception as e:
            logger.warning("xxxxxx [%s] accoured on %s"%(e,item['news_url']))
            #traceback.print_exc()
            
            
            
class TestPipeline(object):
    """
    """

    def process_item(self,item,spider): 
        """
        """
        for k,v in item.items():
            #if k != "content":
            print "%s : %s" % (k,v)

        print "----------------------------\n"

    