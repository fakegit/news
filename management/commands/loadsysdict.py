           #!/usr/bin/env python
#-*-coding:utf-8-*-

# author : "qiulimao"
# email  : "qiulimao@getqiu.com"

""" 
 load jieba system dict.txt
""" 
#---------- code begins below -------
from django.core.management.base import BaseCommand, CommandError
from news.models import Vocabulary
import traceback
import re 

utf8 = lambda s:s.encode("utf-8") if isinstance(s,unicode) else s 

class Command(BaseCommand):
    help = 'load jieba system dict.txt'

    re_userdict = re.compile('^(.+?)(\s+[0-9]+)?(\s+[a-z]+)?\s*$')
    
    def handle(self,*args,**kwargs):
        """
        """
        dictfilepath = "/usr/local/lib/python2.7/dist-packages/jieba/dict.txt"
        try:
            with open(dictfilepath,'r') as f:
                oneline = f.next()
                while oneline:
                    word, freq, tag = self.re_userdict.match(oneline).groups()
                    try:
                        # 第一次导入,都应该不会重复,直接导入,错了再补救
                        newsysword = Vocabulary(word=word,frequency=freq,characteristic=tag,brand="system")
                        newsysword.save()
                    except Exception as e:
                        self.stderr.write("Exception accoured on saving %s" % word)
                    oneline = f.next()
        except StopIteration:
            self.stdout.write("import all the jieba system dict.txt")

        