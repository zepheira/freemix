from django.conf.urls.defaults import *
from freemix.freemixprofile import views
urlpatterns = patterns('',

    url(r'^.*/__history__.html?$',
       views.exhibit_history,
       name='exhibit_history'),

    url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/editor/$',
       views.ExhibitEditorView.as_view(),
       name='exhibit_edit'),

    url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/$',
       views.process_freemix,
       name='exhibit_detail'),

    url(r'^(?P<username>[a-zA-Z0-9_.-]+)/\?build=true&data_profile=(?P<dataset>.+)$',
       views.process_freemix,
       name='build_new_freemix'),

    url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/profile.json$',
       views.exhibit_profile,
       name='exhibit_profile'),

    url(r'^(?P<username>[a-zA-Z0-9_.-]+)/$',
       views.process_freemixes,
       name='freemix_root'),

    url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/embed.js$',
       views.EmbeddedExhibitView.as_view(),
       name='exhibit_embed_js'),

)
