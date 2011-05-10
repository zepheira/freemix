from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site

def get_username(user):
    if isinstance(user,User) and not isinstance(user, AnonymousUser):
        return user.username
    return settings.ANONYMOUS_USERNAME

def get_user(username):
    if username==settings.ANONYMOUS_USERNAME:
        return None
    return get_object_or_404(User,username=username)

from django.http import *

def get_site_url(path="/"):
    return "http://%s%s"%(Site.objects.get_current().domain, path)

# borrowed from http://code.djangoproject.com/wiki/ReplacingGetAbsoluteUrl
import urlparse

class UrlMixin(object):

    def get_url(self):
        if hasattr(self.get_url_path, 'dont_recurse'):
            raise NotImplemented
        try:
            path = self.get_url_path()
        except NotImplemented:
            raise
        return get_site_url(path)
    get_url.dont_recurse = True

    def get_url_path(self):
        if hasattr(self.get_url, 'dont_recurse'):
            raise NotImplemented
        try:
            url = self.get_url()
        except NotImplemented:
            raise
        bits = urlparse.urlparse(url)
        return urlparse.urlunparse(('', '') + bits[2:])
    get_url_path.dont_recurse = True

    def get_absolute_url(self):
        return self.get_url_path()
    def get_site_url(self):
        return get_site_url(self.get_absolute_url())
