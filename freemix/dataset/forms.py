from django import forms
from . import models
from freemix.dataset.models import DataProperty, DataSet
from django.utils.translation import ugettext_lazy as _

class CreateDatasetForm(forms.ModelForm):
    """
    Form for creating a new dataset
    """

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop('owner')
        super(CreateDatasetForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(CreateDatasetForm, self).save(commit=False)
        instance.owner = self.owner
        instance.save()
        return instance

    class Meta:
        model = models.DataSet
        exclude = ("owner",)

class BaseDataPropertyForm(forms.ModelForm):
    "Validates a basic property"

#    property = forms.CharField(label=_("property"),max_length=100)
#    enabled = forms.BooleanField(label = _("enabled"),required=False)
#    label = forms.CharField(max_length=100, label=_("label"))
    type = forms.ChoiceField(label=_("type"))
#    dataset = forms.ModelChoiceField(label = _("dataset"),queryset=DataSet.objects.all())

    class Meta:
        model = DataProperty

    def __init__(self, *args, **kwargs):
        super(BaseDataPropertyForm, self).__init__(*args, **kwargs)
        self.fields["type"].choices = (('',''),) + DataProperty.property_types()


class DataPropertyForm(BaseDataPropertyForm):
    """
    Validates and sets the form instance to the appropriate DataProperty
    subclass.
    """

    _form_registry = {}

    @classmethod
    def register(cls, form):
        "Register a form that validates a particular DataProperty"
        cls._form_registry[form.Meta.model.__name__] = form

    def is_valid(self):
        def validate(self, form):

            if form.is_valid():
                self._meta.model=form._meta.model
                for key in form.fields:
                    self.fields[key] = form.fields[key]
                self.cleaned_data = form.cleaned_data
                self.instance = form.instance
                return True
            return False

        cls = self.instance.__class__.__name__
        if cls != "DataProperty":
            # If we already have a specific property subclass, just validate it
            fc = self._form_registry[cls]
            form = fc(data=self.data, files=self.files)
            form.instance = self.instance
            return validate(self, form)

        if super(DataPropertyForm, self).is_valid():
            for key in self._form_registry:
                # Step through all registered forms until one validates
                form = self._form_registry[key](data=self.data, files=self.files)
                if validate(self, form):
                    return True
            return True # This is a basic property
        return False
