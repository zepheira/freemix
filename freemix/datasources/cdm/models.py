from freemix.dataset.models import DataSource
from django.db import models

class CDMDataSource(DataSource):
    url = models.URLField(verify_exists=False)
    search_term = models.TextField(blank=True)
    collection_name = models.CharField(max_length=255, blank=True)
    
    def __unicode__(self):
        return self.url