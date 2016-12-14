#-*-encoding:utf-8-*-
from django.db import models
from ckeditor.fields import RichTextField
import datetime
from news.settings import RANK_SORT_PARAMETER
# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=128,verbose_name="新闻标题")
    rank = models.IntegerField(verbose_name="新闻ranking")
    news_time = models.DateField(verbose_name="发布时间")
    publisher = models.CharField(max_length=128,verbose_name="新闻来源")
    news_url = models.URLField(verbose_name="新闻网页链接")
    content = RichTextField(verbose_name="新闻内容")
    #add a hash field to unique the news item
    section = models.CharField(max_length=32,verbose_name="分类",default="headline")
    hash_digest = models.CharField(max_length=64,verbose_name="哈希摘要",unique=True)
    cover = models.CharField(max_length=512,verbose_name="封面",default="/static/news/image/newsCover.jpg")
    site = models.CharField(max_length=32,verbose_name="新闻来源",default="getqiu.com")
    
    class Meta:
        verbose_name="新闻"
        verbose_name_plural=verbose_name
        index_together = (("id","news_time","rank"),("section","news_time","rank"),("news_time","rank"))
    def __unicode__(self):
        return u"["+unicode(RANK_SORT_PARAMETER-self.rank)+u"]"+self.title

class NewsStatistic(models.Model):
    news = models.OneToOneField(News,verbose_name="新闻")
    click = models.IntegerField(default=0,verbose_name='点击次数')
    
    class Meta:
        verbose_name="新闻信息统计"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return u"("+unicode(self.click)+u")"+self.news.title    

class TagsNews(models.Model):
    """
     tags 和news 的关系表
    """
    news = models.ForeignKey("News",verbose_name="新闻",on_delete=models.CASCADE)
    tags = models.ForeignKey("Tags",verbose_name="标签",on_delete=models.CASCADE)
    class Meta:
        verbose_name="新闻与标签关系"
        verbose_name_plural = verbose_name
        unique_together = ("news","tags")
        db_table="news_tags_news" # backward capacity
    
    def __unicode__(self):
        return unicode(self.id)     

class Tags(models.Model):
    tag = models.CharField(max_length=32,verbose_name="标签")
    tag_hash = models.CharField(max_length=64,unique=True,verbose_name="标签标示")
    search_times = models.IntegerField(default=0,verbose_name="搜索次数")
    included_items_num = models.IntegerField(default=0,verbose_name="tag所含条目数量")
    #included_items_num其实没必要要。
    news = models.ManyToManyField(News,through="TagsNews",through_fields=("tags","news"),verbose_name="关联内容")
    class Meta:
        verbose_name="标签"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.tag    
    

class Category(models.Model):
    category = models.CharField(max_length=16,verbose_name="分类")
    category_name = models.CharField(max_length=32,null=True,verbose_name="类别")
    news = models.ManyToManyField(News,verbose_name="分类内容")
    class Meta:
        verbose_name="分类"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return self.category    
          

class Suggestion(models.Model):
    visitor = models.GenericIPAddressField(verbose_name='建议者ip')
    time = models.DateTimeField(auto_now_add=True,verbose_name='时间')
    title = models.CharField(max_length=128,verbose_name='建议标题')
    contact = models.CharField(max_length=64,verbose_name='联系方式')
    detail = RichTextField(verbose_name='建议内容')
    
    class Meta:
        verbose_name='建议与意见'
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self.title

class MeaninglessWord(models.Model):
    """
    CREATE TABLE `news_meaninglessword` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `word` varchar(32) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

    alter table news_news add column cover VARCHAR(512) NOT NULL DEFAULT '/static/news/image/newsCover.jpg';

    """
    word = models.CharField(max_length=32,unique=True,verbose_name="词语")

    class Meta:
        verbose_name="Meaningless Word"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.word    

class Settings(models.Model):
    """
    CREATE TABLE `news_settings` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `key` varchar(32) NOT NULL,
    `option` varchar(128) NOT NULL,
    `comment` varchar(512) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_index__key` (`key`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;    
    """
    key = models.CharField(max_length=32,unique=True,verbose_name="option Name")
    option = models.CharField(max_length=128,verbose_name="value",default="0")
    comment = models.CharField(max_length=512,verbose_name="注释",default="COMMENT")
    class Meta:
        verbose_name="settings"
        verbose_name_plural = verbose_name
        #unique_together = ("v1", "v2")

    def __unicode__(self):
        return self.key

class HotWordTrace(models.Model):
    """
    CREATE TABLE `news_hotwordtrace` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `word` varchar(32) NOT NULL,
    `time` date NOT NULL,
    `rank` int(11) NOT NULL,
    `reliable` TINYINT(1) NOT NULL,
    `score` float NOT NULL,
    `note` varchar(128) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `index__time__word__reliable` (`time`,`word`,`reliable`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;      
    """
    word = models.CharField(max_length=32,verbose_name="词语")
    time = models.DateField(auto_now_add=True,verbose_name="推荐时间")
    rank = models.IntegerField(verbose_name="排序",default=0)
    reliable = models.BooleanField(default=True,verbose_name="reliable")
    score = models.FloatField(default=0.0,verbose_name="推荐因子")
    note = models.CharField(max_length=128,verbose_name="备注",default="additional note")
    class Meta:
        verbose_name="hotwordtrace"
        verbose_name_plural = verbose_name
        index_together = ("time","word","reliable")

    def __unicode__(self):
        return self.word


class SearchTrace(models.Model):
    """
    CREATE TABLE `news_searchtrace` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `expression` varchar(32) NOT NULL,
    `time` datetime NOT NULL,
    `day` date NOT NULL,
    `ip` varchar(40) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `index__time` (`time`),
    KEY `index__ip__day` (`ip`,`day`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;     
    """
    expression = models.CharField(max_length=64,verbose_name="搜索表达式")
    time = models.DateTimeField(auto_now=True,verbose_name="搜索时间",db_index=True)
    day = models.DateField(auto_now=True,verbose_name="搜索日期")
    ip = models.CharField(max_length=40,verbose_name="IP 地址")

    @classmethod 
    def getSearchTimeToday(cls,ip):
        """
            get search request times today
        """
        today = datetime.date.today()
        requestTimes = cls.objects.filter(ip=ip,day=today).count()
        return requestTimes
    
    @classmethod
    def getSearchTimeInAll(cls,ip):
        """
            get search time in all
        """
        requestTimes = cls.objects.filter(ip=ip).count()
        return requestTimes

    @classmethod
    def deleteOneDayAgo(cls):
        """
            删除一天以前的记录
        """
        yestoday = datetime.datetime.now() - datetime.timedelta(days=1)
        return cls.objects.filter(time__lte=yestoday).delete()

    class Meta:
        verbose_name="searchTrace"
        verbose_name_plural = verbose_name
        index_together = ("ip","day")

    def __unicode__(self):
        return self.expression    



class Vocabulary(models.Model):
    """
    CREATE TABLE `news_vocabulary` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `word` varchar(16) NOT NULL,
    `frequency` int(11) DEFAULT NULL,
    `characteristic` varchar(8) DEFAULT NULL,
    `brand` varchar(8) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_index__word` (`word`),
    KEY `index__brand__word__id` (`brand`,`word`,`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=40051 DEFAULT CHARSET=utf8
    """
    BRAND=(
        ('system','系统'),
        ('user','自定义'),
    )
    word = models.CharField(max_length="16",verbose_name="词语",unique=True)
    frequency = models.IntegerField(verbose_name="词频",default=2,null=True)
    characteristic = models.CharField(max_length=8,verbose_name="词性",null=True)
    brand = models.CharField(max_length="8",default="user",choices=BRAND,verbose_name="词来源")
    class Meta:
        verbose_name="词典"
        verbose_name_plural = verbose_name
        index_together = (("brand","word","id"),)
        ordering=["-word"]

    def __unicode__(self):
        return self.word 


class Runtime(models.Model):
    """
    CREATE TABLE `news_runtime` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `key` varchar(32) NOT NULL,
    `option` varchar(128) NOT NULL,
    `comment` varchar(512) NOT NULL,
    `time` datetime NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_index__key` (`key`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;    
    """
    key = models.CharField(max_length=32,unique=True,verbose_name="option Name")
    option = models.CharField(max_length=128,verbose_name="value",default="0")
    comment = models.CharField(max_length=512,verbose_name="注释",default="COMMENT")
    time = models.DateTimeField(auto_now=True,verbose_name="更新时间")
    class Meta:
        verbose_name="runtime"
        verbose_name_plural = verbose_name
        #unique_together = ("v1", "v2")

    def __unicode__(self):
        return self.key

    @classmethod
    def getOption(cls,key,default=0,type_=str,comment="some commemnt"):
        """
        """
        try:
            runtimeInstance = cls.objects.get(key=key)
        except cls.DoesNotExist:
            runtimeInstance = cls(key=key,option=str(default),comment=comment)
            runtimeInstance.save()
        return type_(runtimeInstance.option)

    @classmethod
    def setOption(cls,key,option,comment="some commemnt"):
        """
        """
        try:
            runtimeInstance = cls.objects.get(key=key)
            runtimeInstance.option = str(option)
            runtimeInstance.save()
        except cls.DoesNotExist:
            runtimeInstance = cls(key=key,option=str(default),comment=comment)
            runtimeInstance.save()
        