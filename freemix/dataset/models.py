from datetime import datetime, timedelta
import json
import logging
import urllib2
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField

from django.conf import settings
from django.db import models, transaction as db_tx
from django_extensions.db.models import TimeStampedModel
from freemix.transform.conf import AKARA_TRANSFORM_URL
from freemix.transform.views import AkaraTransformClient
from freemix.utils import UrlMixin

logger = logging.getLogger(__name__)


class DataSource(TimeStampedModel):
    classname = models.CharField(max_length=32, editable=False, null=True)

    user = models.ForeignKey(User, related_name="data_sources")

    uuid = UUIDField()

    def get_concrete(self):
        if self.classname == "DataSource":
            return self
        return self.__getattribute__(self.classname.lower())

    def __unicode__(self):
        return self.uuid

    def create_transaction(self, user):
        tx = DataSourceTransaction(source=self)
        tx.save()
        return tx

    def save(self, *args, **kwargs):
        if self.classname is None:
            self.classname = self.__class__.__name__
        super(DataSource, self).save(*args, **kwargs)

class TransformMixin(models.Model):
    transform = AkaraTransformClient(AKARA_TRANSFORM_URL)

    class Meta:
        abstract=True

    def get_transform_params(self):
        return {}

    def get_transform_body(self):
        return None

    def refresh(self):
        return json.dumps(self.transform(body=self.get_transform_body(), params=self.get_transform_params()))


class URLDataSourceMixin(TransformMixin, models.Model):

    url = models.URLField(verify_exists=False)

    class Meta:
        abstract=True

    def get_transform_body(self):
        r = urllib2.urlopen(self.url)
        return r.read()


def make_file_data_source_mixin(storage, upload_to):
    class FileDataSourceMixin(TransformMixin, models.Model):
        file = models.FileField(storage=storage, upload_to=upload_to, max_length=255)
        class Meta:
            abstract=True

        def get_transform_body(self):
            return self.file.read()
    return FileDataSourceMixin
#------------------------------------------------------------------------------#

TX_STATUS = {
    "pending": 1,
    "scheduled": 2,
    "running": 3,
    "success": 4,
    "failure": 5,
    "cancelled": 6
}

TRANSACTION_LIFESPAN = getattr(settings, "TRANSACTION_EXPIRATION_INTERVAL",
                                          timedelta(hours=24))

class DataSourceTransaction(TimeStampedModel, UrlMixin):
    """Stores the the status and raw result of a remote data transaction for a
       particular data source.

       This implementation is temporary, to be replaced with a solution with
       pluggable backends.
    """
    tx_id = UUIDField()

    status = models.IntegerField(choices=[(v,k) for k,v in TX_STATUS.iteritems()],
                                 default=TX_STATUS["pending"])

    source = models.ForeignKey(DataSource, related_name="transactions")

    result = models.TextField(null=True, blank=True)


    def is_expired(self):
        return self.modified < (datetime.now() - TRANSACTION_LIFESPAN)

    @models.permalink
    def get_url_path(self):
        return ('datasource_transaction', (), {
            "tx_id": self.tx_id
        })

    def run(self):
        if self.status != TX_STATUS["pending"]:
            raise

        with db_tx.commit_manually():
            self.status=TX_STATUS["running"]
            self.save()
    #            db_tx.commit()

            try:
                self.result = self.source.get_concrete().refresh()
                self.status=TX_STATUS["success"]
            except Exception as ex:

                logger.error("Error for transaction %s: %s"%(self.tx_id, ex.message))
                self.status=TX_STATUS["failure"]
                self.result = json.dumps({"exception":ex.message})

            self.save()

            db_tx.commit()

        return self
