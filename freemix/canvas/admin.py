from django.contrib import admin
from freemix.canvas.models import Canvas

class CanvasAdmin(admin.ModelAdmin):
        list_display   = ('name', 'description')
        search_fields  = ('name', 'description',)

admin.site.register(Canvas, CanvasAdmin)
