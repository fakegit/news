#-*-encoding:utf-8-*-

from scrapy.spiders import Spider,CrawlSpider,Rule
import scrapy
from crawlers.items import *
from scrapy.loader import ItemLoader
from crawlers.itemLoaders import NewsLoader
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags
from crawlers.items import NewsItem
import re
import datetime
from news.settings import RANK_SORT_PARAMETER
import logging
import gc 
from crawlers.settings import DEFAULT_NEWS_COVER

logger = logging.getLogger(__name__)

class NeteaseSpider(Spider):
    """
      网易新闻的
      每天更新，每次仅需要爬一个页面
    """
    name="163"
    allowed_domains=["money.163.com","tech.163.com","news.163.com","sports.163.com","ent.163.com","auto.163.com",
                     "home.163.com","war.163.com","discovery.163.com","mobile.163.com",
                     "digi.163.com","lady.163.com","edu.163.com","jiankang.163.com","travel.163.com","house.163.com"
    ]
    #allowed_domains = ['jiankang.163.com']
    
    start_urls=["http://money.163.com","http://tech.163.com","http://news.163.com","http://sports.163.com",
                     "http://ent.163.com","http://auto.163.com",
                     "http://home.163.com","http://war.163.com","http://discovery.163.com","http://mobile.163.com",
                     "http://digi.163.com","http://lady.163.com","http://edu.163.com","http://jiankang.163.com",
                     "http://travel.163.com",
                     'http://sports.163.com/nba/','http://money.163.com/stock/',
                     'http://mobile.163.com/iphone/','http://mobile.163.com/android/',"http://cd.house.163.com","http://bj.house.163.com",
                     ]
    #start_urls = ["http://money.163.com/stock/"]
    
    custom_settings={'ITEM_PIPELINES':
            {
              'crawlers.pipelines.NewsPipeline': 300,
              
            }
        }
        
    domain_category_map={
                        'money':'finacial','tech':'technology',
                        'ent':'entertainment','mobile':'mobile',
                        'news':"headline","sports":"sports","auto":"car","home":"home",
                        'war':"military","discovery":"technology","digi":"electronic",
                        'lady':'lady',"edu":"education",'jiankang':'healthy','travel':'travel',
                        'all':'all','other':'other','house':'house'
                        }
        
    def get_info_from_url(self,url):
        """
        """
        infos_in_url = re.search(r'http://([a-z]{1,6}\.)?(?P<category>[a-z]{3,10})\.163\.com/(?P<year>\d{2})/(?P<month>\d{2})(?P<date>\d{2})/\d{2}/\w{16}\.html',url)
        if not infos_in_url:
            return ("other",datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))
        v = infos_in_url.groupdict()
        category_key = v.get('category','other')
        category = self.domain_category_map.get(category_key,'other')
        news_time = "20"+v.get('year','15')+"-"+v.get('month','6')+"-"+v.get('date','6')
        return (category,news_time)
        
        
    def parse(self,response):
        """
        #http://news.163.com/15/1105/03/B7KIM45J00014AED.html
        """
        linkextractor = LinkExtractor(allow=("http://([a-z]{1,6}\.)?[a-z]{3,10}\.163\.com/\d{2}/\d{4}/\d{2}/\w{16}\.html"),
                                        #restrict_css=("body>div.ns-bg-wrap>div.ns-area.cf>div.ns-main>div.ns-mr60")
                                        )
        #在指定区域内抓住的链接，才是想要的链接；采用linkextractor可以有效的抓取想要的链接
        links = linkextractor.extract_links(response)
        for rank,one_link in enumerate(links):
            category,news_time = self.get_info_from_url(one_link.url)
            
            request = scrapy.Request(one_link.url,callback=self.parse_one_news)
            request.meta['rank'] = RANK_SORT_PARAMETER-(rank+1)
            request.meta['category'] = category
            request.meta['news_time'] = news_time
            yield request

        #gc.collect()
            
        
    
    def parse_one_news(self,response):
        """
        """
        news_loader = NewsLoader(item=NewsItem(),response=response)
        #news_loader.add_css('title',"#h1title::text")
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            #news_loader.add_value("title",title)
            news_loader.add_xpath('title','/html/head/title/text()')
        else:
            news_loader.add_xpath("title","//div[@id='epContentLeft']/h1/text()")
            logger.debug("!!!! did't get title on head,parse <%s>'s body instead." % response.url)
            
        news_loader.add_value('rank',str(response.meta['rank']))
        news_loader.add_value('news_time',response.meta['news_time'])
        news_loader.add_css('publisher',"#ne_article_source::text")
        news_loader.add_value("news_url",response.url)


        content = response.xpath("//div[@id='endText']/p[not(style)]").extract()
        if content:
            news_loader.add_xpath('content',"//div[@id='endText']/p[not(style)]")
            cover = response.xpath("//div[@id='endText']/p[not(style)]").xpath(".//img/@src[starts-with(.,'http')]").extract()
            news_cover = cover[0] if cover else DEFAULT_NEWS_COVER
        else:
            news_loader.add_xpath("content","//div[@class='w_text']")
            cover = response.xpath("//div[@class='w_text']").xpath(".//img/@src[starts-with(.,'http')]").extract()
            news_cover = cover[0] if cover else DEFAULT_NEWS_COVER
            logger.debug("!!!! plan A failed,use plan B instead in parsing content <%s>" % response.url)
        
        news_loader.add_value("cover",news_cover)
        news_loader.add_value('category',response.meta['category'])
        #print response.xpath("//title/text()").extract()[0]
        news_loader.add_value("site",u"163.com")
        return news_loader.load_item()
        

class money163(NeteaseSpider):
    name="money_163"
    start_urls=["http://money.163.com",'http://money.163.com/stock/']

class tech163(NeteaseSpider):
    name="tech_163"
    start_urls=["http://tech.163.com"]

class news163(NeteaseSpider):
    name="news_163"
    start_urls=["http://news.163.com"]  

class sports163(NeteaseSpider):
    name="sports_163"
    start_urls=["http://sports.163.com",'http://sports.163.com/nba/']

class ent163(NeteaseSpider):
    name="ent_163"
    start_urls=["http://ent.163.com"]

class auto163(NeteaseSpider):
    name="auto_163"
    start_urls=["http://auto.163.com"]

class home163(NeteaseSpider):
    name="home_163"
    start_urls=["http://home.163.com"]  

class war163(NeteaseSpider):
    name="war_163"
    start_urls=["http://war.163.com"] 

class discovery163(NeteaseSpider):
    name="discovery_163"
    start_urls=["http://discovery.163.com"] 

class mobile163(NeteaseSpider):
    name="mobile_163"
    start_urls=["http://mobile.163.com",'http://mobile.163.com/iphone/','http://mobile.163.com/android/'] 

class digi163(NeteaseSpider):
    name="digi_163"
    start_urls=["http://digi.163.com"]
class lady163(NeteaseSpider):
    name="lady_163"
    start_urls=["http://lady.163.com"] 
class edu163(NeteaseSpider):
    name="edu_163"
    start_urls=["http://edu.163.com"] 
class jiankang163(NeteaseSpider):
    name="jiankang_163"
    start_urls=["http://jiankang.163.com"] 
class travel163(NeteaseSpider):
    name="travel_163"
    start_urls=["http://travel.163.com"]
class house163(NeteaseSpider):
    name="house_163"
    start_urls=["http://bj.house.163.com","http://cd.house.163.com"]    

    