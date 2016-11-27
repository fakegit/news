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
    help = 'find a cover image to the cover field for all the news'

    def handle(self,*args,**kwargs):
        """
        """
        #allNews = News.objects.only("id","content","cover").all()
        newsCount = News.objects.count()
        #newsCount = 10
        dealedItemNumber = 0
        newsid = 1

        while dealedItemNumber < newsCount:
        #for newsid in range(1,11):
            try:
                news = News.objects.only("id","cover","content").get(pk=newsid)

                try:
                    if utf8(news.cover).startswith("http"):
                        # 当前已经有图片了
                        self.stdout.write("<News %d> has aleady have a cover" % newsid)
                        continue

                    newcover = self.find_cover_img(news.content)

                    if newcover.startswith("/static"):
                        # 内容当中没有查出图片来
                        self.stdout.write("<News %d>no image in content use default instead" % news.id)
                        continue

                    News.objects.filter(id=news.id).update(cover=newcover)

                    self.stdout.write("<News %d>'s new cover:%s"%(news.id,newcover))
                except Exception as e:
                    traceback.print_exc()
                    self.stderr.write(self.style.ERROR(u"error in dealing with %s" % news))
                finally:
                    dealedItemNumber = dealedItemNumber + 1
                    newsid = newsid + 1

            except News.DoesNotExist:
                self.stderr.write(self.style.ERROR("<News %d> DOES NOT EXIST!!" % newsid))
                newsid = newsid + 1

        self.stdout.write("[finished] insert a cover to every news in database")

    def find_cover_img(self,input_string):
        DEFAULT_NEWS_COVER = "/static/news/image/newsCover.jpg"
        if not input_string:
            #有些时候，只获取到标题，没有新闻body,不判断要躺枪..
            return DEFAULT_NEWS_COVER
        dom = lxml.html.document_fromstring(input_string)
        covers = dom.xpath("//img/@src[starts-with(.,'http')]")
        news_cover = covers[0] if covers else DEFAULT_NEWS_COVER
        return news_cover        