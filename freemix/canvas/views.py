from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from freemix.canvas.models import Canvas

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
