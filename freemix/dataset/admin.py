from django.forms.models import BaseInlineFormSet
from freemix.dataset.models import DataSet
from django.contrib import admin
from . import models, forms


class BasicDataPropertyFormSet(BaseInlineFormSet):
    def get_queryset(self):
        if not hasattr(self, '_queryset'):
            qs = super(BasicDataPropertyFormSet, self).get_queryset().filter(classname="DataProperty")
            self._queryset = qs
        return self._queryset


class DataPropertyInline(admin.TabularInline):
    model = models.DataProperty
    form = forms.DataPropertyForm
    formset = BasicDataPropertyFormSet

class DataSetAdmin(admin.ModelAdmin):
    list_display   = ('slug','owner',)
    search_fields  = ('slug','title')
    inlines = [DataPropertyInline,]

    @classmethod
    def register_property(cls, inline):
        "Add a property inline to DataSetAdmin.  This should extend DataPropertyInline"
        admin.site.unregister(DataSet)
        cls.inlines += [inline,]
        admin.site.register(DataSet, cls)

admin.site.register(DataSet, DataSetAdmin)
