from django.contrib import admin
from freemix.freemixprofile.models import (Freemix,
                                           ExhibitTheme)


class ExhibitAdmin(admin.ModelAdmin):
    list_display = ('slug', 'user',)
    search_fields = ('slug', 'title', 'description',)

admin.site.register(Freemix, ExhibitAdmin)


class ExhibitThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title', 'description',)

admin.site.register(ExhibitTheme, ExhibitThemeAdmin)
