from django.conf.urls.defaults import patterns, url
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
    url(r'^new/$',login_required(views.DatasetCreateView.as_view()),
        name='dataset_create'),
    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/$',
        views.DatasetListView.as_view(),
        name='dataset_list'
    ),
    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/',
        views.DatasetDetailView.as_view(),
        name='dataset_detail'
    ),
#    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/sources/',
#        views.DataSourceListView.as_view(),
#        name="datasource_list"
#    ),
#
#    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/sources/',
#        views.DataSourceDetailView.as_view(),
#        name="datasource_detail"
#    ),
#    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/sources/new/',
#        views.DataSourceCreateView.as_view(),
#        name="datasource_create"
#    )
)
