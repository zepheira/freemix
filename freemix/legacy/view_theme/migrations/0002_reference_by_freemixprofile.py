
from south.db import db
from django.db import models
import os

class Migration:
    no_dry_run=True
    def forwards(self, orm):
        "Write your forwards migration here"
        if orm.Theme.objects.count() == 0:
            from django.core.management import call_command
            import freemix
            call_command("loaddata",
                         os.path.join(os.path.dirname(models.get_app("view_theme").__file__),
                                      "fixtures/view_themes.json"))

    def backwards(self, orm):
        "Write your backwards migration here"
        pass

    models = {
        'view_theme.theme': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Label'", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'static/images/thumbnails/three-column/smoothness.png'", 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "'/site_media/static/view_theme/smoothness/smoothness.css'", 'max_length': '100'})
        }
    }

    complete_apps = ['view_theme']
