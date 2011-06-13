from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^', include('freemix.dataset.urls.base')),
    (r'^', include('freemix.dataset.urls.viewer')),
    (r'^', include('freemix.dataset.urls.list')),
    (r'^', include('freemix.dataset.urls.editor')),
    (r'tx/', include('freemix.dataset.urls.transaction')),
)
