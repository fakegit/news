#-*-coding:utf-8-*-
#from news import *
from news.models import NewsStatistic
from django.db.models import F

class ClickRecoder():
    
    @classmethod
    def plus_one(self,model_object):
        """
        try:
            followed_news = NewsStatistic.objects.get(news=model_object)
            followed_news.click = followed_news.click+1
            followed_news.save()
            
        except NewsStatistic.DoesNotExist:
            to_track_news = NewsStatistic(news=model_object,click=1)
            to_track_news.save()
        except NewsStatistic.MultipleObjectsReturned:
            NewsStatistic.objects.filter(news=model_object).delete()
        """
        #read_news = NewsStatistic.objects.filter(news=model_object).update(click=F("click")+1)
        track_info_exist = NewsStatistic.objects.filter(news = model_object).exists()
        if track_info_exist:
             NewsStatistic.objects.filter(news=model_object).update(click=F("click")+1)        
        else:
            new_track_info = NewsStatistic(news=model_object,click=1)
            new_track_info.save()
            
            