#-*encoding:utf-8-*
from django.conf.urls import include, url
from . import views

import jieba
from news.utils import build_user_dict

urlpatterns = [
    url(r'^$',views.HomePage.as_view(),name="home_page"),
    url(r'^search/$',views.SearchResult.as_view(),name="search_result"),
    url(r'^news-today/$',views.NewsInToday.as_view(),name="news_today"),
    url(r'^word-trend-api/$',views.WordTrendAPI.as_view(),name="word_trend_api"),
    url(r'^word-trend/$',views.WordTrend.as_view(),name="word_trend"),
    url(r'add-crawler-task/$',views.AddCrawlerTask.as_view(),name="add_crawler_task"),
    url(r'^news-detail/(?P<news_id>[0-9a-zA-Z]{32})/$',views.NewsDetail.as_view(),name="news_detail"),
    url(r'suggestion/$',views.Suggestion.as_view(),name='suggestion'),
    url(r'redirecting/$',views.TransformPage.as_view(),name='transform'),
    url(r'about-us/$',views.AboutUs.as_view(),name='aboutus'),
    url(r'delete-search-record/$',views.DeleteSearchRecord.as_view(),name='delete_search_record'),
]

##
# 启动的时候就重新装载新的字典
##
jieba.load_userdict(build_user_dict())