from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string


class Canvas(models.Model):
    slug = models.SlugField(_('slug'),max_length=100,unique=True)
    name = models.CharField(_('name'), max_length=30, null=False, blank=False, default="Label")
    description = models.CharField(_('description'),max_length=200,null=True, blank=True)
    location = models.CharField(_('location'), unique=True, max_length=100, help_text=_("Example: 'canvas/three-column.html'"))
    thumbnail = models.URLField(_('thumbnail'), verify_exists = False)
    enabled = models.BooleanField(_('enabled'), null=False,default=True)
    
    def get_html(self):
        return render_to_string(self.location, {})
    
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Canvases"
