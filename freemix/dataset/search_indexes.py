import datetime
from haystack.indexes import *
from haystack import site

from . import models

class DataSetIndex(SearchIndex):
    text = CharField(document=True,
                     use_template=True,
                     template_name='search/indexes/dataset/dataset_text.txt')
    modified = DateTimeField(model_attr='modified')
    created = DateTimeField(model_attr='created')
    
    def index_queryset(self):
        return models.DataSet.objects.filter(published=True)


site.register(models.DataSet, DataSetIndex)