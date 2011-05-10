from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields.json import JSONField

from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel

class DataSet(TitleSlugDescriptionModel, TimeStampedModel):
    owner = models.ForeignKey(User, related_name="data_sets")
    published = models.BooleanField(default=True)

    @models.permalink
    def get_absolute_url(self):
        return ("dataset_detail", None, {'owner': self.owner.username,
                                         'slug': self.slug})
    
    class Meta:
        unique_together=('owner', 'slug',)

    def __unicode__(self):
        return self.title


class DataSource(TimeStampedModel):
    classname = models.CharField(max_length=32, editable=False, null=True)
    dataset = models.ForeignKey(DataSet, related_name="sources")
    label = models.CharField(max_length=100, blank=True)
    cached = JSONField()

    def get_concrete(self):
        if self.classname == "DataSource":
            return self
        return self.__getattribute__(self.classname.lower())

    def __unicode__(self):
        if len(self.label) > 0:
            return self.label
        return self.classname.lower()


class UploadedDataSourceMixin(models.Model):
    original_mime_type = models.CharField(max_length=50, null=True,
                                          blank=True, editable=False)
    mime_type_guess = models.CharField(max_length=50, null=True,
                                       blank=True, editable=False)
    mime_type_magic_guess = models.CharField(max_length=50, null=True,
                                             blank=True, editable=False)
    class Meta:
        abstract=True


class DataProperty(models.Model):

    dataset = models.ForeignKey(DataSet, related_name="properties")
    classname = models.CharField(max_length=32, editable=False, null=True)

    type = models.CharField(_("type"),max_length=25)
    enabled = models.BooleanField(_("enabled"),default=True)
    property= models.CharField(_("property"),max_length=100)
    label = models.CharField(_("label"),max_length=100)

    @classmethod
    def get_instance(cls, username, slug, property):
        i = cls.objects.filter(dataset__owner__username=username,
                               dataset__slug=slug, property=property)
        if not i:
            return None
        return i[0].get_concrete()

    def save(self, *args, **kwargs):
        if self.classname is None:
            self.classname = self.__class__.__name__
        super(DataProperty, self).save(*args, **kwargs)

    class Meta:
        unique_together=("dataset", "property")
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        ordering=('id',)

    __type_registry = {}

    def __unicode__(self):
        return self.label

    def get_concrete(self):
        if self.classname == "DataProperty":
            return self
        return self.__getattribute__(self.classname.lower())

    @classmethod
    def property_types(cls):
        return tuple(((slug, cls.__type_registry[slug]) for
                      slug in cls.__type_registry.keys()))

    @classmethod
    def register_type(cls, type, label):
        cls.__type_registry[type] = label

def register_base_properties():
    DataProperty.register_type("text", _("Text"))
    DataProperty.register_type("url", _("URL"))
    DataProperty.register_type("location", _("Location"))
    DataProperty.register_type("image", _("Image"))
    DataProperty.register_type("datetime", _("Date/Time"))

register_base_properties()