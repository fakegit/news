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

class SohuSpider(Spider):
    """
      sohu新闻的
      每天更新，每次仅需要爬一个页面
    """
    name="sohu"

    allowed_domains=["news.sohu.com","mil.sohu.com","business.sohu.com","soyule.sohu.com",
                     "sports.sohu.com","auto.sohu.com","fashion.sohu.com",
                     "it.sohu.com","learning.sohu.com"]
    
    start_urls=["http://news.sohu.com","http://mil.sohu.com","http://business.sohu.com/",
                "http://soyule.sohu.com","http://sports.sohu.com","http://auto.sohu.com/",
                "http://fashion.sohu.com","http://it.sohu.com","http://learning.sohu.com/",
                "http://it.sohu.com/936",
                ]
    #start_urls = ["http://money.163.com/stock/"]
    
    custom_settings={'ITEM_PIPELINES':
            {
              #'crawlers.pipelines.TestPipeline': 302,
              'crawlers.pipelines.NewsPipeline': 302,
              
            }
        }
        
    domain_category_map={
                        'business':'finacial','it':'technology','stock':'finacial',
                        'soyule':'entertainment','mobile':'mobile',
                        'news':"headline","sports":"sports","auto":"car","home":"home",
                        'mil':"military","discovery":"technology","digi":"electronic",
                        'fashion':'lady',"learning":"education",'jiankang':'healthy','travel':'travel',
                        'all':'all','other':'other','house':'house'
                        }
        
    def get_info_from_url(self,url):
        """
        http://news.sohu.com/20170111/n478435011.shtml
        """
        infos_in_url = re.search(r'http://([a-z]{1,6}\.)?(?P<category>[a-z]{3,10})\.sohu\.com/(?P<year>\d{4})(?P<month>\d{2})(?P<date>\d{2})/n\d{9}\.s?html?',url)
        if not infos_in_url:
            return ("other",datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d'))
        v = infos_in_url.groupdict()
        category_key = v.get('category','other')
        category = self.domain_category_map.get(category_key,'other')
        news_time = v.get('year','2016')+"-"+v.get('month','6')+"-"+v.get('date','6')
        return (category,news_time)
        
        
    def parse(self,response):
        """
        #http://news.163.com/15/1105/03/B7KIM45J00014AED.html
        """
        linkextractor = LinkExtractor(allow=("http://([a-z]{1,6}\.)?[a-z]{3,10}\.sohu\.com/\d{4}\d{4}/n\d{9}\.s?html?"),
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
            news_loader.add_xpath('title',"/html/head/title/text()")
        else:
            news_loader.add_xpath("title","//h1[@itemprop='headline']/text()")
            logger.warning("!!!! did't get title on head,parse <%s>'s body instead." % response.url)
            
        news_loader.add_value('rank',str(response.meta['rank']))
        news_loader.add_value('news_time',response.meta['news_time'])
        #news_loader.add_css('publisher',"#ne_article_source::text")
        publisher = response.xpath("//span[@id='media_span']/a/span/text()").extract()

        if publisher and publisher[0]:
            news_loader.add_xpath('publisher',"//span[@id='media_span']/a/span/text()")
        else:
            news_loader.add_value("publisher",u"sohu.com")
        news_loader.add_value("news_url",response.url)


        # content = response.xpath("//div[@id='Cnt-Main-Article-QQ']/p[not(style)]").extract()
        # if content:
        news_loader.add_xpath('content',"//div[@id='contentText']")
        # else:
        #     news_loader.add_xpath("content","//div[@class='w_text']")
        #     logger.warning("!!!! plan A failed,use plan B instead in parsing content <%s>" % response.url)
        
        news_loader.add_value('category',response.meta['category'])
        news_loader.add_value("site",u"sohu.com")

        # 不要到pipeline当中去找这个cover
        cover = response.xpath("//div[@id='contentText']/div[@itemprop='articleBody']").xpath(".//img/@src[starts-with(.,'http')]").extract()
        news_cover = cover[0] if cover else DEFAULT_NEWS_COVER
        news_loader.add_value("cover",news_cover)

        return news_loader.load_item()
        
