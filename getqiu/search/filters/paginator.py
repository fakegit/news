#-*-coding:utf-8-*-

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from news.getqiu.search.context import ViewContext

class PageFilter():
	def __init__(self,item_per_page,request_page=1):
		#self.queryset = queryset
		self.item_per_page = item_per_page
		self.request_page = int(request_page)
	
	def execute(self,view_context):
		"""
			这个函数主要功能将queryset进行分页，默认每页10条记录，客户端代码不可以更改
			更改没有必要
			返回一个和分页相关的结果
		"""
		
		paginator = Paginator(view_context.queryset,self.item_per_page)#设置每页10
		request_page_num = self.request_page
		total_item = paginator.count
		total_page = paginator.num_pages
				
		try:
			one_page_content = paginator.page(request_page_num)
			current_page = request_page_num
		except PageNotAnInteger:
			one_page_content = paginator.page(1)
			current_page = 1
		except EmptyPage:
			one_page_content = paginator.page(paginator.num_pages)
			current_page = paginator.num_pages
			
		next_page = one_page_content.next_page_number() if one_page_content.has_next() else total_page
		prev_page = one_page_content.previous_page_number() if one_page_content.has_previous() else 1
		page_bars = 2#2*page_bars + 设置每页多少10
		
		start_index = current_page-page_bars if current_page>page_bars else 1 
		end_index = start_index +2*page_bars if start_index +2*page_bars < total_page else total_page 

				
		page_context = {'page_info':{
			'current_page':current_page,
			'next_page':next_page,
			'prev_page':prev_page,
			'total_item':total_item,
			'total_page':total_page,
			'pages_indexs':range(start_index,end_index+1)		
		},}
		
		url_parameter_dict = {'page':1}
		
		
		current_view_context =  ViewContext(one_page_content,page_context,url_parameter_dict)
		
		return current_view_context.merge(view_context)