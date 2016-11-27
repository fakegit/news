#-*-coding:utf-8-*-
from django.contrib import admin
from django.forms.widgets import TextInput
# Register your models here.
from .models import *

@admin.register(CrawlerTask,AccountType)
class AuthorAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': TextInput},
    }    
    list_per_page  = 20
    exclude = ['news']    

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
