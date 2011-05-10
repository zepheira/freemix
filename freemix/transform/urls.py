from django.conf.urls.defaults import *
from freemix.transform import views


urlpatterns = patterns('',
    url(r'^file/$', views.FileTransformView(), name="file_transform"),
    url(r'^url/$', views.URLTransformView(), name="url_transform"),
)
