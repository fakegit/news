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
from news.models import News

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
        key_words = jieba.lcut(input_sting)
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

        current_view_context =  ViewContext(final_result.order_by('-news_time','-rank'),search_context,url_parameter_dict)
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
    """
    mysql> explain SELECT 
        `news_news`.`id`, `news_news`.`title`, 
        `news_news`.`rank`, `news_news`.`news_time`, 
        `news_news`.`content` FROM `news_news`
         WHERE (`news_news`.`news_time` >= '2016-03-31' AND `news_news`.`news_time` <= '2016-03-31') 
         ORDER BY `news_news`.`news_time` DESC, `news_news`.`rank` ASC LIMIT 9 OFFSET 18;
        +----+-------------+-----------+------+---------------+------+---------+------+-------+-----------------------------+
        | id | select_type | table     | type | possible_keys | key  | key_len | ref  | rows  | Extra                       |
        +----+-------------+-----------+------+---------------+------+---------+------+-------+-----------------------------+
        |  1 | SIMPLE      | news_news | ALL  | NULL          | NULL | NULL    | NULL | 87368 | Using where; Using filesort |
        +----+-------------+-----------+------+---------------+------+---------+------+-------+-----------------------------+
    1 row in set (0.08 sec)

    after using this index :
        ##
        #  create index search_result_index on news_news(news_time DESC,rank);
        ##
        mysql> explain SELECT 
        `news_news`.`id`, `news_news`.`title`,
         `news_news`.`rank`, `news_news`.`news_time`, 
         `news_news`.`content` FROM `news_news` 
         WHERE (`news_news`.`news_time` >= '2016-03-31' AND `news_news`.`news_time` <= '2016-03-31') 
         ORDER BY `news_news`.`news_time` DESC, `news_news`.`rank` ASC LIMIT 9 OFFSET 18;
        +----+-------------+-----------+-------+---------------------+---------------------+---------+------+------+---------------------------------------+
        | id | select_type | table     | type  | possible_keys       | key                 | key_len | ref  | rows | Extra                                 |
        +----+-------------+-----------+-------+---------------------+---------------------+---------+------+------+---------------------------------------+
        |  1 | SIMPLE      | news_news | range | search_result_index | search_result_index | 3       | NULL |   62 | Using index condition; Using filesort |
        +----+-------------+-----------+-------+---------------------+---------------------+---------+------+------+---------------------------------------+

        1 row in set (0.07 sec)   
        values = Blog.objects.filter(
        name__contains='Cheddar').values_list('pk', flat=True)
            entries = Entry.objects.filter(blog__in=list(values))     
    """

        
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

        key_words = self.find_key_words(self.input_sting)
        key_words_hash = map(lambda x:md5(x.encode('utf-8').lower()).hexdigest(),key_words)
        valid_hash_list = filter(self.filter_out,key_words_hash)
        
        search_context={'search_info':{'search_word':self.input_sting,'searched_words':key_words},}
        url_parameter_dict = {"search_word":self.input_sting}
        if not valid_hash_list:
            current_view_context = ViewContext(self.queryset.none(),search_context,url_parameter_dict)
            return current_view_context.merge(view_context)

        final_result = reduce(self.narrow_queryset,valid_hash_list,self.queryset)
        # 在这个 没有排序过的queryset上做文章
        candidite = [x[0] for x in final_result.values_list("id")]
        #News.objects.filter(id__in=News.object.filter(id__in=final_result))
        # within=Country.objects.filter(continent='Africa').values('mpoly')
        result = News.objects.filter(id__in=candidite).order_by('-id','-news_time','-rank')
        current_view_context =  ViewContext(result,
                                            search_context,url_parameter_dict)
        #current_view_context =  ViewContext(final_result.order_by('-news_time','-rank'),search_context,url_parameter_dict)
        return current_view_context.merge(view_context)
        
    def filter_out(self,one_keyword_hash):
        #queryset_based_on_keyword_hash_exist = self.queryset.filter(tags__tag_hash=one_keyword_hash).exists()
        #if queryset_based_on_keyword_hash_exist:
            #这里花了三条sql，减少到一条
        Tags.objects.filter(tag_hash=one_keyword_hash).update(search_times=F('search_times') + 1)
            #inspect_sql()            
        #return True if queryset_based_on_keyword_hash_exist else False
        return True
        
    def narrow_queryset(self,tmp_queryset,tag_hash):
        return tmp_queryset.filter(tags__tag_hash=tag_hash)
        
    def find_key_words(self,input_sting):
        key_words = jieba.lcut(input_sting)
        #key_words = jieba.cut_for_search(input_sting)
        key_words = list(set(key_words))#去除重复
        key_words = filter(lambda x:False if x in conf.MEANINGLESS_WORDS else True,key_words)
        return key_words
    
