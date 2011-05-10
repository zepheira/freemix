import urllib2
import json
from django.core.cache import cache
from . import conf

def get_akara_version():
    version = cache.get("akara_version")
    if not version:
        version = cache_akara_version()
    return str(version)

def cache_akara_version():
    try:
        version = urllib2.urlopen(conf.AKARA_VERSION_URL).read(100)
    except:
        version = "Unknown"
    cache.set("akara_version", version, 60)
    return version



class AkaraTransformClient(object):
    def __init__(self, url, credentials=None):
        self.akara_url = url
        self.credentials = credentials

    def transform(self, contents, diagnostics=False):
        url = self.akara_url
        if diagnostics:
            url += "?diagnostics=yes"
        if self.credentials:
            auth_handler= urllib2.HTTPDigestAuthHandler()
            auth_handler.add_password(realm=self.credentials[0],
                                      uri=self.akara_url,
                                      user=self.credentials[1], passwd=self.credentials[2])
            opener = urllib2.build_opener(auth_handler)
        else:
            opener=urllib2.build_opener()
        r = urllib2.Request(url, contents)

        data = json.load(opener.open(r))

        return data
