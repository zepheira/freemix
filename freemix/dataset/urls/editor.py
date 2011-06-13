from django.conf.urls.defaults import url, patterns
from django.views.generic.base import TemplateView

# Dataset editor
urlpatterns = patterns('',
    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/editor/$',
        TemplateView.as_view(template_name="dataset/dataset_edit.html"),
        name="dataset_edit"),
)
