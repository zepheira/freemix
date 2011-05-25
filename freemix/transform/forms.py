from django import forms
from django.utils.translation import ugettext_lazy as _


class FileUploadForm(forms.Form):
    file  = forms.FileField()
    diagnostics=forms.BooleanField(required=False, label=_("Verify data"), help_text=_("<a class='verify_data_help' href='#load-info-verify-data'>What's This?</a>"))

class URLUploadForm(forms.Form):
    service_choices = (
        ('', 'None'),
        ('cdm', 'CONTENTdm'),
        #('oai', 'OAI-PMH'),
    )
    url = forms.URLField(required=True, label=_("URL"))
    service = forms.ChoiceField(required=True, label=_("Data service"), choices=service_choices, help_text=_("Leave as 'None' for files or if you are otherwise unsure"))
    cdm_collection_name = forms.CharField(required=False, label=_("Collection name"), help_text=_("Collection names begin with the <strong>/</strong> character"))
    cdm_search_term = forms.CharField(required=False, label=_("Search term"))
    cdm_limit = forms.ChoiceField(label=_("Limit"),
                              help_text=_(
                                  "The maximum number of records to load"),
                              choices=((100, "100"),
                                       (200, "200"),
                                       (300, "300"),
                                       (400, "400")))

    diagnostics=forms.BooleanField(required=False, label=_("Verify data"), help_text=_("<a class='verify_data_help' href='#load-info-verify-data'>What's This?</a>"))

    def clean(self):
        """
        This is essentially a proof of concept since the form validation
        must take place on the client side.  By the time it gets here,
        it must already be valid.
        """
        cleaned = self.cleaned_data
        service = cleaned.get('service')
        cdm_collection = cleaned.get('cdm_collection_name')
        cdm_search = cleaned.get('cdm_search_term')

        if service == 'cdm':
            if cdm_collection == '' and cdm_search == '':
                raise forms.ValidationError(_("A CONTENTdm collection name or search term is required"))

            if cdm_collection != '':
                if cdm_collection[0] != '/':
                    m = _('A CONTENTdm collection name must start with "/"')
                    self._errors["cdm_collection_name"] = self.error_class([m])
                    del cleaned["cdm_collection_name"]

        elif service == 'oai':
            pass

        return cleaned

class ContentDMUploadForm(URLUploadForm):
    cdm_collection_name = forms.CharField(required=False, label=_("Collection name"), help_text=_("Collection names begin with the <strong>/</strong> character"))
    cdm_search_term = forms.CharField(required=False, label=_("Search term"))

