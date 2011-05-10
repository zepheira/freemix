from freemix.dataset.models import UploadedDataSourceMixin, DataSource
from django.db import models

class URLDataSource(DataSource, UploadedDataSourceMixin):
    url = models.URLField(verify_exists=False)

    def __unicode__(self):
        return self.url