#-*-coding:utf-8-*-
from news.models import NewsStatistic,News
import jieba
import jieba.analyse
import datetime

class HotWords():
    
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
            hotest_news = News.objects.filter(news_time__range=(yesterday,today)).first()
            title = hotest_news.title
            #解决初始化没有值的问题
        except Exception:
            hotest_news = News.objects.order_by('-news_time','rank').first()
            title = hotest_news.title
        return jieba.analyse.extract_tags(title)[0:10]#最多10个关键词
        