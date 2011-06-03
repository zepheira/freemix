from django.conf.urls.defaults import *
from freemix.freemixprofile import views
urlpatterns = patterns('',

                       url(r'^.+/.+/__history__.html/?$',
                           views.exhibit_history,
                           name='freemix_exhibit_history'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/\?build=true$',
                           views.build_freemix,
                           name='build_freemix'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/$',
                           views.process_freemix,
                           name='view-freemix'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/\?build=true&data_profile=(?P<dataset>.+)$',
                           views.process_freemix,
                           name='build_new_freemix'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/profile.json$',
                           views.freemix_metadata,
                           name='freemix_metadata'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$',
                           views.process_freemixes,
                           name='freemix_root'),

                       url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/embed.js$',
                           views.EmbeddedExhibitView.as_view(),
                           name='freemix-embed-script'),

                       )
