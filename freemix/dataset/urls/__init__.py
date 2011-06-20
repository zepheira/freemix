from django.conf import settings
from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',

    (r'tx/', include('freemix.dataset.urls.transaction')),
    (r'^', include('freemix.dataset.urls.base')),
    (r'^', include('freemix.dataset.urls.viewer')),
    (r'^', include('freemix.dataset.urls.list')),
    (r'^', include('freemix.dataset.urls.editor')),
)

if "freemix.freemixprofile" in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        (r'^', include('freemix.freemixprofile.urls.dataset')),
    )