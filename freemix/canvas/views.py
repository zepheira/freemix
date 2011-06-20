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

def canvas_list(request, template_name="canvas/list.json"):
    obj_list = Canvas.objects.filter(enabled=True)
    return render_to_response(template_name, {"canvas_list": obj_list},
            context_instance=RequestContext(request))


def canvas_css(request, template_name="canvas/canvas.css"):
    response = render_to_response(template_name, {},
            context_instance=RequestContext(request))
    response['Content-Type'] = "text/css"
    return response

def canvas_html(request, slug):
    canvas = get_object_or_404(Canvas,slug=slug)
    return render_to_response(canvas.location, {},
            context_instance=RequestContext(request))
