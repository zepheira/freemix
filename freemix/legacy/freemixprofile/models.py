from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import resolve
from django_extensions.db.models import (TimeStampedModel,
                                         TitleSlugDescriptionModel)
from django.utils.translation import ugettext_lazy as _
from freemix.dataset.models import Dataset

from freemix.utils import get_user, get_username
from freemix.legacy.canvas.models import Canvas
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


def create_exhibit(user, dataset, contents):
    text = contents.get("text", {})
    title = text.get("title", "")
    description = text.get("subtitle")

    canvas = get_object_or_404(Canvas, slug=contents["canvas"])
    theme = get_object_or_404(ExhibitTheme, slug=contents["theme"])

    exhibit = Freemix.objects.create(user=user,
                                     dataset=dataset,
                                     canvas=canvas,
                                     theme=theme,
                                     title=title,
                                     description=description,
                                     json=contents)

    return exhibit


class Freemix(TitleSlugDescriptionModel, TimeStampedModel):
    user = models.ForeignKey(User, null=True)
    json = JSONField()
    dataset = models.ForeignKey(Dataset, null=True, blank=True)
    canvas = models.ForeignKey(Canvas)
    theme = models.ForeignKey(ExhibitTheme, default=0)

    def natural_key(self):
        return self.user, self.slug

    @models.permalink
    def get_absolute_url(self):
        return ('exhibit_detail', (), {
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

    def dataset_available(self, user):
        """True if the provided user is able to view the dataset associated with this exhibit
        """
        ds = self.dataset
        if not ds or not user.has_perm("dataset.can_view", ds):
            return False
        return True

    class Meta:
        unique_together = ("slug", "user")
        verbose_name_plural = "Exhibits"
        verbose_name = "Exhibit"
        ordering = ('-modified', )
