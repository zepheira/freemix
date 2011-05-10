from django.conf.urls.defaults import *
from .views import *

urlpatterns = patterns('',

                       url(r'^.+/.+/__history__.html/?$',
                           exhibit_history,
                           name='freemix_exhibit_history'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/\?build=true$',
                           build_freemix,
                           name='build_freemix'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/$',
                           process_freemix,
                           name='view-freemix'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/\?build=true&data_profile=(?P<dataset>.+)$',
                           process_freemix,
                           name='build_new_freemix'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/profile.json$',
                           freemix_metadata,
                           name='freemix_metadata'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$',
                           process_freemixes,
                           name='freemix_root'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/embed.js$',
                           embed_exhibit,
                           name='freemix-embed-script'),

                       )
