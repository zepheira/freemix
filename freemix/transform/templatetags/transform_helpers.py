from django import template
from freemix.transform.views import get_akara_version
from freemix.transform.conf import AKARA_URL_PREFIX

register = template.Library()

@register.simple_tag
def akara_version():
    return get_akara_version()

@register.simple_tag
def akara_prefix_url():
    return AKARA_URL_PREFIX
