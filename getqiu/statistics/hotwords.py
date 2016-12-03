#-*-coding:utf-8-*-
from news.models import NewsStatistic,News,MeaninglessWord,Settings,HotWordTrace
import jieba
import jieba.analyse
import jieba.posseg
import datetime
from collections import Counter
import re
from itertools import ifilter
import datetime 
from news.configure import getDBConfigure

utf8 = lambda s:s.encode("utf-8") if isinstance(s,unicode) else s 

class HotWords():
    regex_verb = r'[v]'
    regex_number = r'[m]+'
    regex_allowed = r'(nr|nt|nz)'
    denied_words = set()


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
        ##
        # get configure from database
        #   
        #   RECOMM_DAYS = 2
        #   RECOMM_RANK_GT = 200
        #   RECOMM_NEWSLIMIT = RECOMM_DAYS * RECOMM_RANK_GT
        #   RECOMM_HALF_DESC = 30
        #   RECOMM_NUM = 8
        #   这里的配置不用设置缓存时间，每次直接实时读数据库就好
        ##
 
        RECOMM_DAYS = getDBConfigure("RECOMM_DAYS",default=2,type_=int)
        RECOMM_RANK_GT = getDBConfigure("RECOMM_RANK_GT",default=200,type_=int)

        RECOMM_NEWSLIMIT = RECOMM_DAYS * RECOMM_RANK_GT

        RECOMM_HALF_DESC = getDBConfigure("RECOMM_HALF_DESC",default="30.0",type_=float)
        RECOMM_NUM = getDBConfigure("RECOMM_NUM",default=8,type_=int)

        RECOMM_RECORD_HOT = getDBConfigure("RECOMM_RECORD_HOT",default=0,type_=lambda v:bool(int(v)))

        RECOMM_ALLOWED_WORD_TYPE_REGEX = getDBConfigure("RECOMM_ALLOWED_WORD_TYPE_REGEX",default="(nr|nz|nt)",type_=str)

        # 设置词性的正则表达式
        cls.regex_allowed = re.compile(RECOMM_ALLOWED_WORD_TYPE_REGEX)
        ############END SETTINGS FORM DATABASE#################
        today = datetime.date.today()
        oneday = datetime.timedelta(days=RECOMM_DAYS) 
        yesterday=today - oneday         
        recent_news = News.objects.filter(news_time__gte=yesterday,news_time__lte=today,rank__gt=(1000-200))\
                                  .only("title")\
                                  .order_by("-news_time").all()[0:RECOMM_NEWSLIMIT]
        #tagList = []
        tagMap = dict()
        for news in recent_news:
            tags = jieba.posseg.cut(news.title)
            tags = filter(cls.filter_out_short,tags)
            #tags = filter(cls.filter_out_verb,tags)
            tags = filter(cls.filter_out_number,tags)
            tags = filter(cls.filter_out_deny,tags)
            tags = filter(cls.filter_in_only,tags)
            #map(lambda t:cls.upsert(t,news.rank,tagMap),tags)
            for tag in tags:
                score = RECOMM_HALF_DESC/(1000-news.rank+int(RECOMM_HALF_DESC))
                key = tag.word

                if tagMap.has_key(key):
                    tagMap[key] = score + tagMap[key]
                else:
                    tagMap[key] = score  
                #print "[%d]the score for %s is %f" % (news.rank,key,tagMap[key])
        #counter = Counter(tagList)
        #print "the length of tagList is %d" % len(tagList)
        hot_word_tube = sorted(tagMap.items(),key=lambda x:x[1],reverse=True)
        #hot_word_tube = counter.most_common(8)
        #hot_words = [ str(x[0])+"/"+str(x[1]) for x in hot_word_tube]
        hot_words = [ x[0] for x in hot_word_tube[0:RECOMM_NUM]]

        # 根据是否开启热词记录
        if RECOMM_RECORD_HOT:
            for i,w in enumerate(hot_word_tube[0:RECOMM_NUM]):
                try:
                    hotword = HotWordTrace.objects.only("word")\
                                          .get(time=datetime.date.today(),word=w[0])
                except HotWordTrace.DoesNotExist:
                    note="using %s/(1+%s)" % (RECOMM_HALF_DESC,RECOMM_HALF_DESC) # for debug popurse
                    hotword = HotWordTrace(word=w[0],rank=i+1,score=w[1],note=note)
                    hotword.save()
                except HotWordTrace.MultipleObjectsReturned:
                    hotword = HotWordTrace.objects.only("id")\
                                          .filter(time=datetime.date.today(),word=w[0])
                    theSameId = [x[0] for x in hotword.values_list("id")[1:]]
                    HotWordTrace.objects.filter(id__in=theSameId).delete()
                    
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
        if re.match(cls.regex_allowed,tag.flag):
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
            
        