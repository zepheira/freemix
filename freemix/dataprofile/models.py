import json

from django.template.defaultfilters import slugify
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_extensions.db.models import (TimeStampedModel,
                                         TitleSlugDescriptionModel)
from freemix.utils import get_username
from freemix.utils import UrlMixin
from django_extensions.db.fields.json import JSONField


import uuid

def create_dataset(user, contents, slug=None):
    profile = contents.get("data_profile", contents)
    title = profile.get("label", slug)
    profile['original_MIME_type'] = profile.get("Akara_MIME_type_guess")

    data_profile = DataProfile.objects.create(user=user,
                                              title=title,
                                              properties={"properties": profile["properties"]},
                                              original_mime_type=profile.get("original_MIME_type"),
                                              mime_type_guess=profile.get("Akara_MIME_type_guess"),
                                              mime_type_magic_guess=profile.get("Akara_MIME_type_magic_guess"))
    if "items" in contents:
        data_profile.save_file("data.json", {"items": contents["items"]})
    return data_profile


class DataProfile(TitleSlugDescriptionModel, TimeStampedModel, UrlMixin):
    user = models.ForeignKey(User, null=True, related_name="data_sets")
    properties = JSONField()
    original_mime_type = models.CharField(max_length=50, null=True, blank=True)
    mime_type_guess = models.CharField(max_length=50, null=True, blank=True)
    mime_type_magic_guess = models.CharField(max_length=50, null=True,
                                             blank=True)

    def __unicode__( self ):
        return self.title

    def natural_key(self):
        return [self.user,self.title]


    @models.permalink
    def get_url_path(self):
        return ('dataset_viewer', (), {
            'username': get_username(self.user),
            'slug': self.slug
        })

    def get_profile_url(self):
        return reverse("dataset_profile",
                              kwargs={ "username": self.user.username,
                                  "slug": self.slug})
    def update_profile(self, contents):
        profile = contents.get("data_profile", contents)
        self.title= profile.get("label", self.slug)
        self.properties = {"properties": profile.get("properties")}
        self.original_mime_type = profile.get("original_MIME_type")
        self.mime_type_guess = profile.get("Akara_MIME_type_guess")
        self.mime_type_magic_guess = profile.get("Akara_MIME_type_magic_guess")
        self.save()
        if "items" in contents:
            self.save_file("data.json", {"items": contents["items"]})

    def get_dict(self):
        dict = self.properties
        dict["label"] = self.title
        dict["url"] = reverse('dataset_data',
                              kwargs={ "username": self.user.username,
                                  "slug": self.slug})
        dict["original_MIME_type"] = self.original_mime_type
        dict["Akara_MIME_type_guess"] = self.mime_type_guess
        dict["Akara_MIME_type_magic_guess"] = self.mime_type_magic_guess
        return dict

    def merge_data(self):
        result = []
        def find(d):
            for item in result:
                if d.get("label") == item.get("label") and \
                   d.get("id") == item.get("id"):
                    return item
            return None

        for file in self.data_files.all():
            for data in file.json["items"]:
                r = find(data)
                if r:
                    r.update(data)
                else:
                    result.append(data)
        return {"items": result}

    def everything(self):
        return {"data_profile": self.get_dict(), "items":
                  self.merge_data()["items"]}

    def save_file(self, filename, contents):
        file,created = DataFile.objects.get_or_create(name=filename,
                                              data_profile=self)
        file.json=contents
        file.save()

    class Meta:
        unique_together=("slug", "user")
        verbose_name_plural = "Data Sets"
        verbose_name = "Data Set"
        ordering = ('-modified', )

class DataFile(TimeStampedModel):

    name = models.CharField(max_length=200)
    json = JSONField()
    data_profile = models.ForeignKey(DataProfile, related_name="data_files")
    __registry = {}

    class Meta:
        unique_together=(("name", "data_profile"),)

    @classmethod
    def file_types(cls):
        return ((slug, cls.__registry[slug]) for slug in cls.__registry.keys())

    @classmethod
    def register(cls, filename, label):
        cls.__registry[filename] = label



DataFile.register("data.json", "Transformed Data")
