from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.template import Variable
from freemix.freemixprofile import models

register = template.Library()


@register.inclusion_tag("exhibit/exhibit_summary.html", takes_context=True)
def exhibit_summary(context, exhibit):
    request = context['request']
    visible = exhibit.dataset_available(request.user)
    return {"exhibit": exhibit, "request": request, "visible": visible}

@register.inclusion_tag("exhibit/exhibit_list.html", takes_context=True)
def dataview_list(context, queryset, max_count=10, pageable=True):
    return {"queryset": queryset, "max_count": max_count, "pageable": pageable,
            "request": context['request']}

@register.inclusion_tag("exhibit/exhibit_create_dialog.html", takes_context=True)
def new_dataview(context):
    return {'STATIC_URL': settings.STATIC_URL}

# Theme tags
@register.tag
def theme_list(parser, token):
    return ThemeListNode("view_theme/list.html" )

@register.tag
def theme_css_link(parser, token):
    try:
        tag_name, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents[0]
    return ThemeLinkNode(slug)

class ThemeListNode( template.Node ):
    def __init__ (self, template):
        self.template = template

    def render(self, context):
        return render_to_string(self.template, {"theme_list": models.ExhibitTheme.objects.filter(enabled=True)})

class ThemeLinkNode( template.Node ):
    def __init__(self, slug):
        self.slug = slug

    def render(self, context):
        slug = Variable(self.slug).resolve(context)
        theme = models.ExhibitTheme.objects.get(slug=slug)
        return "<link rel='stylesheet' href='%s' type='text/css' />"%theme.url

