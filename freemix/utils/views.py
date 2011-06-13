from django.http import *
from django.views.defaults import *
from django.views.generic.base import View
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
import json

# RESTResource and JSONResponse poached from http://www.djangosnippets.org/snippets/1740/

class RESTResource(object):
    """
    Dispatches based on HTTP method.
    """
    # Possible methods; subclasses could override this.
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def __call__(self, request, *args, **kwargs):
        callback = getattr(self, request.method, None)
        if callback:
            return callback(request, *args, **kwargs)
        else:
            allowed_methods = [m for m in self.methods if hasattr(self, m)]
            return HttpResponseNotAllowed(allowed_methods)

class JSONResponse(HttpResponse):

    def __init__(self, data, template=None,**extra_context):
        indent = 2 if settings.DEBUG else None

        if template:
            context = {"json": json.dumps(data, indent=indent)}
            if extra_context:
                context.update(extra_context)
            content = render_to_string(template, context)
            mime = "application/javascript"
        else:
            content = json.dumps(data, indent=indent)
            mime = ("text/javascript" if settings.DEBUG
                                  else "application/json")
        super(JSONResponse, self).__init__(
            content = content,
            mimetype = mime,
        )

class JSONView(View):

    template=None
    def get_dict(self, *args, **kwargs):
        return {}

    def get(self, *args, **kwargs):
        content = self.get_dict(*args, **kwargs)
        return JSONResponse(content, self.template)


class LegacyListView(RESTResource):
    def __init__(self, template=None, filter_func=None, extra_context_func=None,
                annotate=None):
        if template:
            self.template = template
        if filter_func:
            self.get_queryset = filter_func
        if extra_context_func:
            self.extra_context = extra_context_func

    def GET(self, request, *args, **kwargs):
       context = kwargs.copy()
       extra_context_func = getattr(self, "extra_context", None)
       if extra_context_func:
           context.update(extra_context_func(request, **kwargs))
       objects = self.get_objects(request, **context)
       context["queryset"] = objects

       return render_to_response(self.template, context ,
            context_instance=RequestContext(request))

    def get_objects(self, request, **kwargs):
        results = self.get_queryset(request, **kwargs)
        annotate = getattr(self, "annotations", None)
        if annotate:
            results = annotate(request, results)
        return results
