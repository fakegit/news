#-*-coding:utf-8-*-
from news.models import NewsStatistic,News
import jieba
import jieba.analyse

class HotWords():
	
	@classmethod
	def read_most(self):
		try:
			hotest_news = NewsStatistic.objects.order_by('-news__news_time','-click','news__rank').first()
			title = hotest_news.news.title
			#解决初始化没有值的问题
		except Exception:
			hotest_news = News.objects.order_by('-news_time','rank').first()
			title = hotest_news.title
		return jieba.analyse.extract_tags(title)[0:10]#最多10个关键词
		