from django.conf import settings
from django.conf.urls.defaults import url, patterns
from freemix.dataset import  views

# Dataset List URLs
urlpatterns = patterns('',
    url(r"^(?P<owner>[a-zA-Z0-9_.-]+)/$",
        views.dataset_list_by_owner,
        name="dataset_list_by_owner"
    ),
)

if "freemix.freemixprofile" in settings.INSTALLED_APPS:
    from freemix.freemixprofile.views import exhibits_by_dataset
    urlpatterns += (
        url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/views.html$',
            exhibits_by_dataset,
            name='exhibits_by_dataset'
        ),
    )