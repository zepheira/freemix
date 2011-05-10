from django.conf.urls.defaults import *

urlpatterns = patterns('freemix.canvas.views',
    url(r'^list\.json', 'canvas_list', name='canvas_list_json'),
    url(r'^list\.html', 'canvas_list', {"template_name":"canvas/list.html"},name='canvas_list_html'),
    url(r'^canvas\.css', 'canvas_css', name='canvas_css'),
    url(r'^((?P<slug>.+)\.html$)', 'canvas_html', name='canvas_html'),
#    url(r'^((?P<slug>.+)/sample\.html$)', 'canvas_sample', name='canvas_sample'),
)
