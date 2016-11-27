#-*-coding:utf-8-*-
from news.models import NewsStatistic,News,MeaninglessWord
import jieba
import jieba.analyse
import jieba.posseg
import datetime
from collections import Counter
import re
from itertools import ifilter

utf8 = lambda s:s.encode("utf-8") if isinstance(s,unicode) else s 

class HotWords():
    regex_verb = r'[v]'
    regex_number = r'[m]+'
    regex_allowed = r'[rjt]+'
    denied_words = set()
    # ['中国','曝光','男子','女子','明年','今天','昨天']

    @classmethod
    def init(cls):
        cls.getDeniedWordsSet()

    @classmethod
    def getDeniedWordsSet(cls):
        meaningless = MeaninglessWord.objects.all()
        for w in meaningless:
            cls.denied_words.add(utf8(w.word))
        return cls.denied_words
        
    @classmethod
    def read_most(self):
        """
        SELECT `news_newsstatistic`.`id`, `news_newsstatistic`.`news_id`, `news_newsstatistic`.`click` FROM `news_newsstatistic` INNER JOIN `news_news` ON ( `news_newsstatistic`.`news_id` = `news_news`.`id` ) ORDER BY `news_news`.`news_time` DESC, `news_newsstatistic`.`click` DESC, `news_news`.`rank` ASC LIMIT 1;
        对应的sql非常可怕，慎用：
        mysql> explain SELECT `news_newsstatistic`.`id`, `news_newsstatistic`.`news_id`, `news_newsstatistic`.`click` FROM `news_newsstatistic` INNER JOIN `news_news` ON ( `news_newsstatistic`.`news_id` = `news_news`.`id` ) ORDER BY `news_news`.`news_time` DESC, `news_newsstatistic`.`click` DESC, `news_news`.`rank` ASC LIMIT 1;
        +----+-------------+--------------------+--------+---------------+---------+---------+---------------------------------+-------+---------------------------------+
        | id | select_type | table              | type   | possible_keys | key     | key_len | ref                             | rows  | Extra                           |
        +----+-------------+--------------------+--------+---------------+---------+---------+---------------------------------+-------+---------------------------------+
        |  1 | SIMPLE      | news_newsstatistic | ALL    | news_id       | NULL    | NULL    | NULL                            | 22490 | Using temporary; Using filesort |
        |  1 | SIMPLE      | news_news          | eq_ref | PRIMARY       | PRIMARY | 4       | news.news_newsstatistic.news_id |     1 | NULL                            |
        +----+-------------+--------------------+--------+---------------+---------+---------+---------------------------------+-------+---------------------------------+        
        """
        try:
            #hotest_news = NewsStatistic.objects.order_by('-news__news_time','-click','news__rank').first()
            today = datetime.date.today()
            oneday = datetime.timedelta(days=1) 
            yesterday=today - oneday 
            hotest_news = News.objects.filter(news_time__gt=yesterday).filter(news_time__lt=today).first()
            title = hotest_news.title
            #解决初始化没有值的问题
        except Exception:
            hotest_news = News.objects.order_by('-news_time','-rank').first()
            title = hotest_news.title
        return jieba.analyse.extract_tags(title)[0:10]#最多10个关键词

    @classmethod
    def appear_most(cls):
        """
            查找tilte当中出现最多的关键词
        """
        cls.init()

        today = datetime.date.today()
        oneday = datetime.timedelta(days=3) 
        yesterday=today - oneday         
        recent_news = News.objects.filter(news_time__gt=yesterday,news_time__lt=today).only("title").order_by("-news_time").all()[0:500]
        tagList = []
        for news in recent_news:
            tags = jieba.posseg.cut(news.title)
            tags = filter(cls.filter_out_short,tags)
            #tags = filter(cls.filter_out_verb,tags)
            tags = filter(cls.filter_out_number,tags)
            tags = filter(cls.filter_out_deny,tags)
            tags = filter(cls.filter_in_only,tags)
            map(lambda t:tagList.append(t.word),tags)
        
        counter = Counter(tagList)
        #print "the length of tagList is %d" % len(tagList)

        hot_word_tube = counter.most_common(8)
        #hot_words = [ str(x[0])+"/"+str(x[1]) for x in hot_word_tube]
        hot_words = [ x[0] for x in hot_word_tube]
        return hot_words

    @classmethod
    def filter_out_deny(cls,tag):
        """
        """
        if utf8(tag.word) in cls.denied_words:
            return False
        return True 

    @classmethod
    def filter_in_only(cls,tag):
        if re.search(cls.regex_allowed,tag.flag):
            return True
        return False 

    @classmethod
    def filter_out_short(cls,tag):
        """
        """
        if len(tag.word) >=2:
            return True
        return False


    @classmethod
    def filter_out_verb(cls,tag):
        """
            过滤非名字,并且长度必须大于2
        """
        if not re.search(cls.regex_verb,tag.flag):
            return True
        return False

    @classmethod
    def filter_out_number(cls,tag):
        """
            过滤数字
        """
        if re.search(cls.regex_number,tag.flag):
            return False
        return True
            
        