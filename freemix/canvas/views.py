from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.views.generic.base import View, TemplateView
from freemix.canvas.models import Canvas
from freemix.dataset.models import Dataset

class CanvasChooserView(View):
    template_name = "canvas/chooser.html"

    def get(self, request, *args, **kwargs):
        obj_list = Canvas.objects.filter(enabled=True)
        ds = get_object_or_404(Dataset, owner__username = kwargs["owner"],slug = kwargs["slug"])
        return render(request, self.template_name, {
            "canvases": obj_list,
            "base_url": reverse("exhibit_create_editor", kwargs={"owner": kwargs["owner"],
                                                                 "slug":kwargs["slug"]})
        })
