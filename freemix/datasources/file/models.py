from freemix.dataset.models import UploadedDataSourceMixin, DataSource
from django.db import models

class FileDataSource(DataSource, UploadedDataSourceMixin):
    filename = models.CharField(max_length=50, editable=False)

    def __unicode__(self):
        return self.filename
