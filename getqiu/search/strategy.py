#-*-coding:utf-8-*-
class SearchStrategy(object):
    """
    搜索策略类
    """
    def search(self,keywords_list,model_manager):
        #这个类必须要实现search方法
        #keywords_list 是关键词
        #model_manager为数据库中所有数据的queryset
        #函数必须要返回一个queryset
        pass


class AddStrategy(SearchStrategy):
    
    def get_item_by_and(self,queryset,key_word):
        tmp_queryset = queryset.filter(title__contains=key_word)
        return tmp_queryset    
    

    def search(self,keywords_list,model_manager):
        #add 逻辑直接采用reduce简单又快捷
        return  reduce(self.get_item_by_and,keywords_list,model_manager)    