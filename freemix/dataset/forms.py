from django import forms
from freemix.dataset.models import Dataset

class CreateDatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        