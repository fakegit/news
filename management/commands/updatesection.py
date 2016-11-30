#!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 find the cover
""" 
#---------- code begins below -------
from django.core.management.base import BaseCommand, CommandError
from news.models import News
import lxml.html 
import traceback

utf8 = lambda s:s.encode("utf-8") if isinstance(s,unicode) else s 

class Command(BaseCommand):
    help = 'update news_news.section field'

    def handle(self,*args,**kwargs):
        """
        """
        newsCount = News.objects.count()
        #newsCount = 10
        dealedItemNumber = 0
        newsid = 1L
        while dealedItemNumber < newsCount:
        #for newsid in range(1,11):
            try:
                news = News.objects.only("id","section").get(id=newsid)

                news_section = news.category_set.first().category
                if utf8(news_section).startswith("headline"):
                    newsid = newsid + 1
                    dealedItemNumber = dealedItemNumber + 1
                    continue
                News.objects.filter(id=newsid).update(section=news_section)
                self.stdout.write("<News %d>add section infomation" % news.id)
                newsid = newsid + 1
                dealedItemNumber = dealedItemNumber + 1
            except News.DoesNotExist:
                self.stderr.write(self.style.ERROR("<News %d> DOES NOT EXIST!!" % newsid))
                newsid = newsid + 1

        self.stdout.write("Update all in database")