#-*-encoding:utf-8-*-
from django import forms
from .models import Suggestion
from ckeditor.widgets import CKEditorWidget
#from django.forms import ModelForm

class AddCrawlerTaskForm(forms.ModelForm):
    """
    """
    pass
    
    
class SearchBoxForm(forms.Form):
    search_word = forms.CharField(label = u"搜索",max_length = 20,widget=forms.TextInput({'class':'form-control'}))
    start_time = forms.DateField(label=u'开始时间',required=False,widget = forms.DateInput({'class':'form-control ','type':'date'}))
    end_time = forms.DateField(label=u'截止时间',required=False,widget = forms.DateInput({'class':'form-control','type':'date'}))    
    
class TestForm(forms.Form):
    field1 = forms.CharField(label=u'field1',max_length=20,widget=forms.TextInput({'class':'form-control','placeholder':"field1"}))    
    field2 = forms.CharField(label=u'field2',max_length=20,widget=forms.TextInput({'class':'form-control','placeholder':"field2"}))        
    
    
class SuggestionForm(forms.ModelForm):
    """
     这个错误太TM RG!!!真的查不出来！！！！！！
     为什么在这里加CSS的样式不可以！！！
    """
    #required_css_class = 'col-md-2'
    class Meta:
        model = Suggestion 
        fields = ('title','contact','detail')
        
        widgets = {
            'title':forms.TextInput({'placeholder':'标题','class':'form-control'}),
            'contact':forms.TextInput({'placeholder':'留下您的联系方式，采纳会有礼品','class':'form-control'})
        }    


class TimeWindowForm(forms.Form):
    """
    """
    start_time = forms.DateField(label=u'开始时间',required=False)
    end_time = forms.DateField(label=u'截止时间',required=False)

class MigrateRelationForm(forms.Form):
    oldtag = forms.CharField(label = u"旧tag",max_length = 8,widget=forms.TextInput({'class':'form-control'}))
    newtag = forms.CharField(label=u'新tag',max_length=8,widget = forms.TextInput({'class':'form-control'}))