#-*-encoding:utf-8-*-

from scrapy.spiders import Spider,CrawlSpider,Rule
import scrapy
from crawlers.items import *
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider
from scrapy.linkextractors import LinkExtractor

class ZhixingSpider(Spider):
    """
    """
    name="zhixing"
    allowed_domains=["zhixing.bjtu.edu.cn"]
    start_urls=['http://zhixing.bjtu.edu.cn']
    
    rules = (
        Rule(LinkExtractor(allow=('.+thread.+'),deny=(),restrict_css=("#portal_block_620_content")),callback='main_page',follow=True),
        Rule(LinkExtractor(allow=(),restrict_css=("#pgt>div>div>a.nxt")),callback="current_page",follow=True),
    )
    

    def parse(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username':'qiulimao25', 'password':'00qiulimao44'},
            callback=self.after_login
        )
    
    def after_login(self,response):
        #myinfo = response.css("#um > p:nth-child(2) > strong > a::text").extract()[0]
        #print myinfo
        links_e = LinkExtractor(allow=('.+thread.+'),deny=(),restrict_css=("#portal_block_620_content"))
        links = links_e.extract_links(response)
        for one_link in links:
            yield scrapy.Request(one_link.url,callback=self.current_page)
        
        
            
    
    def current_page(self,response):
        current_page = response.css("#pgt > div > div > strong::text").extract()[0]
        subject = response.css("#thread_subject::text").extract()[0]
        author = response.xpath("//*[@id='pgt']/div/div/label/span/text()").extract()[0]
        print ">>>>>>>>>>>>>>"+current_page,author,subject