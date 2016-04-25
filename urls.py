#-*encoding:utf-8-*
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.HomePage.as_view(),name="home_page"),
    url(r'^search/$',views.SearchResult.as_view(),name="search_result"),
    url(r'^news-today/$',views.NewsInToday.as_view(),name="news_tody"),
    url(r'add-crawler-task/$',views.AddCrawlerTask.as_view(),name="add_crawler_task"),
    url(r'^news-detail/(?P<news_id>[0-9a-zA-Z]{32})/$',views.NewsDetail.as_view(),name="news_detail"),
    url(r'suggestion/$',views.Suggestion.as_view(),name='suggestion'),
    url(r'redirecting/$',views.TransformPage.as_view(),name='transform'),
    url(r'about-us/$',views.AboutUs.as_view(),name='aboutus'),
]
