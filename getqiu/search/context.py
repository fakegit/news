#-*-coding:utf-8-*-
import urllib

class ViewContext(object):
    """
    """
    
    def __init__(self,queryset,context,url_parameter_dict,*args,**kargs):
        
        self.queryset = queryset
        
        self.url_parameter_dict = url_parameter_dict
        self.context_dict = dict(context)
        
        self.args = args
        self.kargs = kargs
        
    def build_url(self,exclude_key):
        """
        首先将字典的每一个值作成utf-8
        
        """
        m = lambda x:x.encode('utf-8') if isinstance(x,unicode) else x
        encode_to_url_value = {key:m(value) for key,value in self.url_parameter_dict.items() if key != exclude_key}
        return urllib.urlencode(encode_to_url_value)
        
    def build_url_to_context(self,exclude_key):
        """
            将 url_parameter_dict 当中的字段用于构造成为一个url.
            例如:在分页的地方需要这样的url:
               /search_result/?search_word=xxx&category=all&page=1
               /search_result/?search_word=xxx&category=all&page=2
               显然排除掉page这个字段需要自己构造，其他字段在后台自动合并生成就好
        """
        encoded_url = self.build_url(exclude_key)
        if self.context_dict.has_key('encoded_url'):
            self.context_dict['encoded_url'] = dict(self.context_dict['encoded_url'],**{exclude_key:encoded_url})
        else:
            self.context_dict['encoded_url'] = {exclude_key:encoded_url}
            
    def build_urls_to_context(self,key_list):
        
        map(self.build_url_to_context,key_list)
        
    def add_queryset_to_context(self):
        self.context_dict = dict(self.context_dict,**{'model_objects':self.queryset})
    
    def merge(self,another_viewcontext):
        news_queryset = self.queryset
        #谁merge 保留谁的queryset，因为返回的queryset只能一个
        new_context = dict(self.context_dict,**another_viewcontext.context)
        new_url_parameter_dict = dict(self.url_parameter_dict,**another_viewcontext.url_parameter_dict)
        return ViewContext(news_queryset,new_context,new_url_parameter_dict,*self.args,**self.kargs)
        
        
    @property    
    def context(self):
        """
        """
        
        self.build_urls_to_context(self.url_parameter_dict.keys())
        self.add_queryset_to_context()
        
        return self.context_dict
        
        
        
        
