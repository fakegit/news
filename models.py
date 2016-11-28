#-*-encoding:utf-8-*-
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=128,verbose_name="新闻标题")
    rank = models.IntegerField(verbose_name="新闻ranking")
    news_time = models.DateField(verbose_name="发布时间")
    publisher = models.CharField(max_length=128,verbose_name="新闻来源")
    news_url = models.URLField(verbose_name="新闻网页链接")
    content = RichTextField(verbose_name="新闻内容")
    #add a hash field to unique the news item
    hash_digest = models.CharField(max_length=64,verbose_name="哈希摘要",unique=True)
    cover = models.CharField(max_length=512,verbose_name="封面",default="/static/news/image/newsCover.jpg")
    
    class Meta:
        verbose_name="新闻"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return str(self.rank)+"-|_"+self.title

class NewsStatistic(models.Model):
    news = models.OneToOneField(News,verbose_name="新闻")
    click = models.IntegerField(default=0,verbose_name='点击次数')
    
    class Meta:
        verbose_name="新闻信息统计"
        verbose_name_plural=verbose_name
    def __unicode__(self):
        return "("+str(self.click)+")"+self.news.title    

class Tags(models.Model):
    tag = models.CharField(max_length=32,verbose_name="标签")
    tag_hash = models.CharField(max_length=64,unique=True,verbose_name="标签标示")
    search_times = models.IntegerField(default=0,verbose_name="搜索次数")
    included_items_num = models.IntegerField(default=0,verbose_name="tag所含条目数量")
    #included_items_num其实没必要要。
    news = models.ManyToManyField(News,verbose_name="关联内容")
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
    
class CrawlerTask(models.Model):
    """
        任务列表当中 如何去解析任务？
    """
    TASK_TYPE = (
        ('1',"长期任务"),
        ('0','一次性任务'),
    )
    
    task_type = models.CharField(max_length=10,choices = TASK_TYPE,default='1',verbose_name="任务类型")
    #url = models.URLField(verbose_name="目标URL地址")
    execute_time = models.DateTimeField(verbose_name="执行时间")
    account_type = models.ForeignKey('AccountType',verbose_name="帐号类型")
    account = models.CharField(max_length = 128,default='get_site_info',verbose_name="监视帐号")
    class Meta:
        verbose_name="爬虫任务类表"
        verbose_name_plural = verbose_name
        
    def __unicode__(self):
        return self.account_type.account+"  "+self.account
        
class AccountType(models.Model):
    
    COMPLEX_LEVEL = (
        ('0','随意爬取'),
        ('1','需要登录'),
        ('2','登录+验证码'),
        ('3','验证码识别困难'),
        ('4','登录机制复杂'),
        ('5','需人工模式'),
    )
    account = models.CharField(max_length=128,verbose_name="账户类型")
    complex_level = models.CharField(max_length=16,choices=COMPLEX_LEVEL,verbose_name="复杂度")
    
    class Meta:
        verbose_name="支持网站"
        verbose_name_plural = "支持网站"
        
    def __unicode__(self):
        return self.account
        
        

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
    word = models.CharField(max_length=32,verbose_name="词语")

    class Meta:
        verbose_name="meaningless word"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.word    