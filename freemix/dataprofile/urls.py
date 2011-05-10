from django.conf.urls.defaults import url, patterns
from freemix.freemixprofile.views import dataviews_by_dataset

username_pattern = r"^(?P<username>[a-zA-Z0-9_.-]+)/"
dataset_pattern = r"%s(?P<slug>[a-zA-Z0-9_.-]+)/"%username_pattern

urlpatterns = patterns('freemix.dataprofile.views',

    url(r'upload/$',
        'upload_dataset',
        name='upload_dataset'),

    url(r'%s$'%username_pattern,
        'datasets_by_user',
        name='user_datasets'),

    url(r'%spublish/$'%username_pattern,
        'publish_dataset',
        name='publish_dataset'),

    url(r'%sprofile.json$'%dataset_pattern,
        'dataset_profile',
        name='dataset_profile'),

    url(r'%sdata.json$'%dataset_pattern,
        'transformed_data',
        name='dataset_data'),

    url(r'%sexport.json$'%dataset_pattern,
       'merged_dataset',
       name='merged_dataset'),

    url(r'%seditor/data.jsonp$'%dataset_pattern,
       'editor_jsonp',
       name='dataset_editor_jsonp'),
    url(r'%sviewer/data.jsonp$'%dataset_pattern,
       'viewer_jsonp',
       name='dataset_viewer_jsonp'),

    url(r'%seditor/$'%dataset_pattern,
        'edit_dataset',
        name='edit_data_set'),


    url(r'%s$'%dataset_pattern,
        'dataset_view',
        name='dataset_viewer'),

    url(r'%severything.json'%dataset_pattern,
       'everything_json',
       name='everything_json'),
)

urlpatterns += (
    url(r'^(?P<username>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/views.html$',
        dataviews_by_dataset,
        name='dataviews_by_dataset'
       ),
)
