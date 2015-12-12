#-*-coding:utf-8-*-
import jieba
import jieba.analyse
from itertools import chain
from news.getqiu.search.strategy import AddStrategy
from news.getqiu.search.context import ViewContext		
from hashlib import md5
from django.db.models import Q,F
#from django.db.models import F
from news.models import Tags
from django.db import connection
from news.getqiu.search import  conf


def print_dict(item):
	for key,value in item.items():
		print key+":\n"+value+"\n"
		
def inspect_sql():
	queries = connection.queries[-2:]
	for one_sql in queries:	
		print_dict(one_sql)

class TitleBasedEngine(object):
	"""
	Poll.objects.get(
    Q(question__startswith='Who'),
    Q(pub_date=date(2005, 5, 2)) | Q(pub_date=date(2005, 5, 6))
    )
	"""
	
	def __init__(self,input_sting,search_strategy=AddStrategy()):
		"""
		queryset 为所使用的model
		search_strategy 是一个搜索策略类
                if isinstance(queryset,QuerySet):
                    self.queryset = queryset
                elif isinstance(queryset,ViewContext):
                    self.queryset = queryset.queryset
                #写一个搜索的父类，父类存在一个方法，如果第一个参数是viewcontext，那么返回viewcontext时，自动合并viewcontext
		"""
		#self.queryset = queryset
		self.search_strategy = search_strategy
		self.input_sting = input_sting

		
	def find_key_words(self,input_sting):
		"""
		使用jieba库，拆分出句子当中的关键词
		"""
		key_words = jieba.analyse.extract_tags(input_sting)
		return key_words
				
	def execute(self,view_context):
		"""
		  	搜索，客户端代码直接调用，返回一个queryset
			search_strategy改为由search方法指定
			这样可以实例化一个strategy对象，应用多个法则
		"""
		self.queryset = view_context.queryset
		key_words = self.find_key_words(self.input_sting)
		valid_words_list = filter(self.filter_out,key_words)
		#以上查看是否存在可 参与搜索的关键词
		search_context={'search_info':{'search_word':self.input_sting,'searched_words':valid_words_list},}
		url_parameter_dict = {'search_word':self.input_sting}
		if not valid_words_list:
			#没有就直接返回一个空
			current_view_context =  ViewContext(self.queryset.none(),search_context,url_parameter_dict)
			return current_view_context.merge(view_context)
			
		#search_manager = self.queryset.all()
		#实际上将搜索的逻辑关系委托给了searchStrategy这个类
		final_result = self.search_strategy.search(valid_words_list,self.queryset)

		current_view_context =  ViewContext(final_result.order_by('-news_time','rank'),search_context,url_parameter_dict)
		return current_view_context.merge(view_context)
		
		
			
	def filter_out(self,one_keyword):
		"""
		 这个方法用于过滤关键词，看看数据库中是不是有这样的关键词，没有的直接滤过
		"""
		if one_keyword in conf.MEANINGLESS_WORDS:
			return False
		queryset_based_on_keyword_exist = self.queryset.filter(title__contains=one_keyword).exists()
		#print "sql query:"+str(queryset_based_on_keyword.query)
		if queryset_based_on_keyword_exist:
			return True
		else:
			return False
	
		


class TagBasedSearch(TitleBasedEngine):
	

		
	def execute(self,view_context):
		
		self.queryset = view_context.queryset
		key_words = self.find_key_words(self.input_sting)
		key_words_hash = map(lambda x:md5(x.encode('utf-8').lower()).hexdigest(),key_words)
		valid_hash_list = filter(self.filter_out,key_words_hash)
		
		search_context={'search_info':{'search_word':self.input_sting,'searched_words':key_words},}
		url_parameter_dict = {"search_word":self.input_sting}
		if not valid_hash_list:
			current_view_context = ViewContext(self.queryset.none(),search_context,url_parameter_dict)
			return current_view_context.merge(view_context)
		final_result = reduce(self.narrow_queryset,valid_hash_list,self.queryset)
		
		current_view_context =  ViewContext(final_result.order_by('-news_time','rank'),search_context,url_parameter_dict)
		return current_view_context.merge(view_context)
		
	def filter_out(self,one_keyword_hash):
		queryset_based_on_keyword_hash_exist = self.queryset.filter(tags__tag_hash=one_keyword_hash).exists()
		if queryset_based_on_keyword_hash_exist:
			#这里花了三条sql，减少到一条
			Tags.objects.filter(tag_hash=one_keyword_hash).update(search_times=F('search_times') + 1)
			#inspect_sql()			
		return True if queryset_based_on_keyword_hash_exist else False
		
	def narrow_queryset(self,tmp_queryset,tag_hash):
		return tmp_queryset.filter(tags__tag_hash=tag_hash)
		
	def find_key_words(self,input_sting):
		key_words = jieba.cut_for_search(input_sting)
		return [word for word in key_words]
	
