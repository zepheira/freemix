from django.contrib import admin
from .models import DataProfile, DataFile
from .forms import DataFileForm

class DataFileInline(admin.TabularInline):
    model=DataFile
    form=DataFileForm
    extra=0

class DataProfileAdmin(admin.ModelAdmin):
    list_display   = ('slug','user',)
    search_fields  = ('slug','name')
    inlines=[DataFileInline,]
admin.site.register(DataProfile, DataProfileAdmin)

