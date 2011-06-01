from django import forms
from django.utils.translation import ugettext_lazy as _


class FileUploadForm(forms.Form):
    file = forms.FileField()


class URLUploadForm(forms.Form):
    url = forms.URLField(required=True, label=_("URL"))

