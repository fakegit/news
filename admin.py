#-*-coding:utf-8-*-
from django.contrib import admin
from django.forms.widgets import TextInput
# Register your models here.
from .models import *
 

class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag','included_items_num','search_times')
    list_per_page = 100
    exclude=['news']
    
admin.site.register(Tags,TagsAdmin)

class ClickCountInline(admin.StackedInline):
    model = NewsStatistic
    can_delete =  False
    verbose_name = "访问次数"

    
class NewsAdmin(admin.ModelAdmin):
    """
    """
    list_display=('title','news_time','rank')
    list_per_page  = 20  
    inlines = (ClickCountInline,)
    #search_fields = ["=tags__tag",]
    #ordering = []
    #list_filter = ('news_time',"category__category")
    #exclude = ['news']

admin.site.register(News,NewsAdmin)  

class CategoryAdmin(admin.ModelAdmin):
    """
    """
    exclude = ['news']

admin.site.register(Category,CategoryAdmin) 

class SuggestionAdmin(admin.ModelAdmin):
    """
    """
    list_display=('title','time')
    list_per_page = 20
    
admin.site.register(Suggestion,SuggestionAdmin)

class MeaningLessWordAdmin(admin.ModelAdmin):
    """
    """
    list_per_page=30

admin.site.register(MeaninglessWord,MeaningLessWordAdmin)

class SettingsAdmin(admin.ModelAdmin):
    """
    """
    list_display=('key','option',"comment")
    list_per_page=30
    search_fields = ["key",'comment']
    ordering = []

admin.site.register(Settings,SettingsAdmin)



class HotWordTraceAdmin(admin.ModelAdmin):
    """
    """
    list_display=('time','word',"score","rank")
    list_per_page=30

admin.site.register(HotWordTrace,HotWordTraceAdmin)


class SearchTraceAdmin(admin.ModelAdmin):
    """
    """
    list_display=('ip','expression',"time")
    list_per_page=30

admin.site.register(SearchTrace,SearchTraceAdmin)