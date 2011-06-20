from django.conf.urls.defaults import *

urlpatterns = patterns('freemix.canvas.views',
    url(r'^canvas\.css', 'canvas_css', name='canvas_css'),
    url(r'^((?P<slug>.+)\.html$)', 'canvas_html', name='canvas_html'),
)
