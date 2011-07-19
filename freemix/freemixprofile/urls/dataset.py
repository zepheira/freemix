# URL patterns for linking exhibits to their dataset

from django.conf.urls.defaults import url
from django.contrib.auth.decorators import login_required
from freemix.freemixprofile.views import CanvasChooserView

from freemix.freemixprofile.views import exhibits_by_dataset, StockExhibitProfileJSONView, NewExhibitEditorView


urlpatterns = (
    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/views.html$',
        exhibits_by_dataset,
        name='exhibits_by_dataset'
    ),
    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/view/profile.json$',
        StockExhibitProfileJSONView.as_view(),
        name='exhibit_profile_template'
    ),
    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/view/$',
        login_required(NewExhibitEditorView.as_view()),
        name='exhibit_create_editor'
    ),
    url(r'^(?P<owner>[a-zA-Z0-9_.-]+)/(?P<slug>[a-zA-Z0-9_.-]+)/view/canvases.html',
        CanvasChooserView.as_view(),
        name='exhibit_canvas_chooser'
    )
)