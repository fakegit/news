#-*-coding:utf-8-*-
import jieba
import jieba.analyse
from news.models import Tags,News
from django.db.models import F
from hashlib import md5
import re
from news.getqiu.search import  conf


class AddTag():
	"""
	meaningless_words = set([u'我',u'的',u'“',u'；',u'、',u'，',u'。',u'-',u' ',
		u'吗',u'哦',u'于',u'把',u'也',u'》',u"《",u'',u'仅',u'+',u'哪',u'/',
		u'仍',u'但',u'？',u'?',u'～',u'!',u'@',u'#',u'$',u'%',u'￥',u'……',
		u'*',u'（',u'）',u'<',u'>',u'了',u'有',u'”',u'：',u'1',u'2',u'"',
		u'之',u'者',u'哉',u'.',u'(',u')',u'[',u'`',u'|',u'\\',u'/',u']',u'{',u'}',
		u'『',u'』',u'-',u'-',u'_',u'一',u'',u':',u'',
	])
	"""
	meaningless_words = conf.MEANINGLESS_WORDS
	def __init__(self,model_object,field):
		"""
		model_object :将要创建tag来索引的对象实例
		field :采用哪个字段来创建 tag
		addtag has only one method :save()
		"""
		self.model_object = model_object
		self.field = field
	
	def save(self):
		#jieba.loaduserdict(filename)
		#tags = jieba.analyse.extract_tags(self.__get_to_extract_string())
		tags_iteral = jieba.lcut_for_search(self.__get_to_extract_string())
		#使得唯一
		tags = filter(self.pickout_words,set(tags_iteral))
		#map(self.__connect_tag_with_object,tags)
		tags_objects = map(self.__create_tag_object,tags)
		self.model_object.tags_set.add(*tags_objects)
		#return self.model_object
		#礼尚往来，返回一个model_object把，目前不知道会有什么作用
		
		
		
	
	def __get_to_extract_string(self):
		return self.model_object.__getattribute__(self.field)
	
	def pickout_words(self,word):
		if word in self.meaningless_words:
			return False
		if re.search(r'^\d+\.?\d+$',word):
			return False
		if re.search(r'^[A-Za-z0-9]$',word):
			return False
		return True
		
	def __create_tag_object(self,tag):
		#这个方法可以被子类重写，但是必须范围一个tag的instance
		# 怎么返回tag，这是子类的问题，但是通常，一定要保证tag唯一
		#所以继承的这个类，最好现查以下数据库，看看这个tag是否已经存在了
		hash_value = md5(tag.encode('utf-8').lower()).hexdigest()
		#news_exist = News.objects.only('id').filter(id=self.model_object.id).exists()
		#首先计算tag的hash值。
		try:
			tag_object = Tags.objects.only("included_items_num").get(tag_hash=hash_value)
			#if not news_exist:
			Tags.objects.filter(tag_hash=hash_value).update(included_items_num=F('included_items_num') + 1)
			#	tag_object.included_items_num = tag_object.included_items_num + 1
			#	tag_object.save()
			#在数据库中查一下，是否已经存在这个tag了
		except Tags.DoesNotExist:
			#没有？那么就创建这么一个tag
			tag_object = Tags(tag=tag.encode('utf-8'),tag_hash=hash_value,included_items_num=1)
			tag_object.save()
			
		return tag_object
		
	def __connect_tag_with_object(self,a_tag):
		#save_a_tag 
		a_tag_object = self.__create_tag_object(a_tag)
		if self.model_object.tags_set.filter(id=a_tag_object.id).exists():
			pass
		else:
			a_tag_object.included_items_num = a_tag_object.included_items_num + 1
			a_tag_object.save()		
			#a_tag_object.news.add(self.model_object)
			#优化的部分主要在这里，要不考虑多个tag一次性加入，可能会减少数据库hit
			self.model_object.tags_set.add(a_tag_object)
		return 1
		
		
		
		
		
