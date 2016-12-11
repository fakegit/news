#-*-coding:utf-8-*-
import jieba
import jieba.analyse
from itertools import chain
from news.getqiu.search import strategy
from news.getqiu.search.strategy import NormalOrder,InQueryBasedOrder
from news.getqiu.search.context import ViewContext        
from hashlib import md5
from django.db.models import Q,F
#from django.db.models import F
from news.models import Tags
from django.db import connection
from news.getqiu.search import  conf
from news.models import News
from news.configure import getMaxCountForSearchResult as maxcount
from news.configure import getSearchStrategy

class TagBasedSearch(object):
    """
        基于标签的检索
    """
    def __init__(self,input_sting):
        """
        """
        self.input_sting = input_sting
        
    def execute(self,view_context):
        WILD_CARD = "*"

        self.queryset = view_context.queryset
        #----deal with wild card *
        if self.input_sting == WILD_CARD:
            search_context={'search_info':{'search_word':self.input_sting,'searched_words':WILD_CARD},}
            url_parameter_dict = {"search_word":self.input_sting}
            ordered_result = self.queryset.order_by('-news_time','-rank')
            current_view_context = ViewContext(ordered_result,search_context,url_parameter_dict)
            return current_view_context.merge(view_context)

        # 分词
        key_words = self.find_key_words(self.input_sting)

        # 过滤无效词
        valid_word = filter(self.filter_out,key_words)
        
        search_context={'search_info':{'search_word':self.input_sting,'searched_words':key_words},}
        url_parameter_dict = {"search_word":self.input_sting}
        if not valid_word:
            # 没有结果的情况
            current_view_context = ViewContext(self.queryset.none(),search_context,
                                               url_parameter_dict,resultcount=0)
            return current_view_context.merge(view_context)

        # 执行搜索
        qualified_result = reduce(self.narrow_queryset,valid_word,self.queryset)

        # 设置排序器
        queryStrategy = getSearchStrategy()
        if hasattr(strategy,queryStrategy):
            rankOrder = getattr(strategy,queryStrategy)(qualified_result)
        else:
            # 设置错误回到默认
            rankOrder = getattr(strategy,"InQueryBasedOrder")(qualified_result)

        current_view_context =  ViewContext(rankOrder.result,
                                            search_context,
                                            url_parameter_dict,
                                            resultcount=rankOrder.count)

        return current_view_context.merge(view_context)
        
    def filter_out(self,one_keyword):
        """
            update函数如果没有影响到列,那么返回0,所以根据这个可以统计搜索次数,还能过滤无效词
        """
        updatedCount = Tags.objects.filter(tag=one_keyword).update(search_times=F('search_times') + 1)           
        return True if updatedCount else False
        
    def narrow_queryset(self,tmp_queryset,tag):
        """
            缩小queryset范围
        """
        return tmp_queryset.filter(tags__tag=tag)
        
    def find_key_words(self,input_sting):
        """
            分词,并去除停用词
        """
        key_words = jieba.lcut(input_sting)
        #key_words = jieba.cut_for_search(input_sting)
        key_words = list(set(key_words))#去除重复
        key_words = filter(lambda x:False if x in conf.MEANINGLESS_WORDS else True,key_words)
        return key_words
    
