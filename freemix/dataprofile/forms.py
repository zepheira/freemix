from django import forms
from .models import DataFile

class DataFileForm(forms.ModelForm):

    name=forms.ChoiceField()
    
    def __init__(self, *args, **kwargs):
        super(DataFileForm, self).__init__(*args, **kwargs)
        self.fields["name"].choices = DataFile.file_types()
        
    
    class Meta:
        model=DataFile
    
