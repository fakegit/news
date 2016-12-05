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
        with open(dictfilepath,'r') as f:
            oneline = f.next()
            while oneline:
                word, freq, tag = self.re_userdict.match(oneline).groups()
                try:
                    word = Vocabulary.objects.get(word=word)
                except Vocabulary.DoesNotExist:
                    newsysword = Vocabulary(word=word,frequency=freq,characteristic=tag,brand="system")
                    newsysword.save()

                oneline = f.next()

        self.stdout.write("import all the jieba system dict.txt")