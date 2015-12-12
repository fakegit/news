#-*-encoding:utf-8-*-
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join,Compose,Identity
import re
from w3lib.html import remove_tags
import datetime

def extract_time(str_content):
	"""
            从指定的句子当中提取出时间
	"""
	find_time = re.search('(\d{4}-\d{2}-\d{2})',str_content)
	if find_time:
		return find_time.group(0)
	else:
        #没找到就默认当前的时间
		return datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
def clean_title(str_content):
	"""
		直接从标题中提取title。去除163
	"""
	cleaned_string=re.sub(r'_网易.*$','',str_content.encode('utf-8'))
	return cleaned_string.decode('utf-8')	

def strip_blank(str_content):
	#scrapy 将所有爬取到的内容都转换为unicode,而正则处理的str和buff类型
	#所以先将 unicode转换为utf-8.但是处理完成以后，需要返回unicode，方便其他processor使用
	cleaned_string = re.sub(r'\s',"",str_content.encode('utf-8'))
	return cleaned_string.decode('utf-8')
	
def remove_colon(str_content):
	#道理同strip_black，处理：时，附带将字符串头尾的空白去除【因为不要无故去除字符串中间的空格】
	cleaned_string =  re.sub(r'^.*：|\s+$',"",str_content.encode('utf-8'))
	return cleaned_string.decode('utf-8')
	
class NewsLoader(ItemLoader):
	"""
	"""
        #默认最终拼接成一个字符串
	default_output_processor = Join()
        #Compose是将整个list传给第一个processors处理后的结果给第二个processors，然后第三个...
	#news_time_in = Compose(TakeFirst(),extract_time,)
        #MapCompose是将整个list传个一个processor,processors对list中的每个元素处理，结果在给第二个processors
	content_in = Identity()#MapCompose(remove_tags,)
	title_in = MapCompose(unicode.strip,clean_title)
	