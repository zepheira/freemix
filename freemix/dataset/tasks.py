import json
from urllib import urlencode
import urllib2
from celery.task import task
from . import conf
from freemix.dataset.models import DataSource

@task(name="dataset.tasks.url_transform")
def url_transform(source_id, diagnostics=False):
    source = DataSource.objects.get(id=source_id)
    
    

@task()
def transform():
    pass


class AkaraTransformClient(object):
    def __init__(self, url, credentials=None):
        self.akara_url = url
        self.credentials = credentials

    def transform(self, url, params=None, body=None):
        if params is None:
            params = {}
        if self.credentials:
            auth_handler= urllib2.HTTPDigestAuthHandler()
            auth_handler.add_password(realm=self.credentials[0],
                                      uri=url,
                                      user=self.credentials[1],
                                      passwd=self.credentials[2])
            opener = urllib2.build_opener(auth_handler)
        else:
            opener=urllib2.build_opener()
        r = urllib2.Request('%s?%s' % (url, urlencode(params)), body)
        data = json.load(opener.open(r))
        return data
