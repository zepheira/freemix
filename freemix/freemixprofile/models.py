from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import resolve
from django_extensions.db.models import (TimeStampedModel,
                                         TitleSlugDescriptionModel)
from django.utils.translation import ugettext_lazy as _

from freemix.utils import get_user, get_username
from freemix.utils import UrlMixin
from freemix.dataprofile.models import DataProfile
from freemix.canvas.models import Canvas
from django_extensions.db.fields.json import JSONField


class ExhibitTheme(TitleSlugDescriptionModel, models.Model):
    url = models.URLField(_('url'), unique=False, max_length=100,
                          help_text=_("Example: '/static/view_theme"
                                      "/smoothness/smoothness.css'"),
                          default="/static/view_theme/"
                                  "smoothness/smoothness.css",
                          verify_exists=False)
    thumbnail = models.ImageField(_('thumbnail'), upload_to='view_theme/img',
                                  default="static/images/thumbnails"
                                          "/three-column/smoothness.png")
    enabled = models.BooleanField(_('enabled'), null=False, default=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")


def create_exhibit(user, contents, exhibit_id=None):
    text = contents.get("text", {})
    title = text.get("title", "")
    description = text.get("subtitle")

    url = contents["dataProfile"]
    view, args, kwargs = resolve(url)
    profile_user = get_user(kwargs["username"])
    profile = get_object_or_404(DataProfile,
                                user=profile_user,
                                slug=kwargs["slug"])

    canvas = get_object_or_404(Canvas, slug=contents["canvas"])
    theme = get_object_or_404(ExhibitTheme, slug=contents["theme"])

    exhibit = Freemix.objects.create(user=user,
                                     data_profile=profile,
                                     canvas=canvas,
                                     theme=theme,
                                     title=title,
                                     description=description,
                                     json=contents)

    return exhibit


class Freemix(TitleSlugDescriptionModel, TimeStampedModel, UrlMixin):
    user = models.ForeignKey(User, null=True, related_name="data_views")
    json = JSONField()
    data_profile = models.ForeignKey(DataProfile, related_name="data_views")
    canvas = models.ForeignKey(Canvas)
    theme = models.ForeignKey(ExhibitTheme, default=0)

    def natural_key(self):
        return self.user, self.slug

    @models.permalink
    def get_url_path(self):
        return ('view-freemix', (), {
            'username': get_username(self.user),
            'slug': self.slug})

    # Overridden for RSS/Atom feeds
    def __unicode__(self):
        return self.title

    def update_profile(self, contents):
        text = contents.get("text", {})
        self.title = text.get("title")
        self.description = text.get("subtitle")
        self.canvas = get_object_or_404(Canvas, slug=contents["canvas"])
        self.theme = get_object_or_404(ExhibitTheme, slug=contents["theme"])
        self.json = contents
        self.save()

    class Meta:
        unique_together = ("slug", "user")
        verbose_name_plural = "Exhibits"
        verbose_name = "Exhibit"
        ordering = ('-modified', )
