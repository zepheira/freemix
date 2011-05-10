
from south.db import db
from django.db import models
from freemix.canvas.models import *

class Migration:

    def forwards(self, orm):

        # Adding field 'Canvas.thumbnail'
        db.add_column('canvas_canvas', 'thumbnail', orm['canvas.canvas:thumbnail'])



    def backwards(self, orm):

        # Deleting field 'Canvas.thumbnail'
        db.delete_column('canvas_canvas', 'thumbnail')



    models = {
        'canvas.canvas': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Label'", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'images/thumbnails/three-column/smoothness.png'", 'max_length': '100'})
        }
    }

    complete_apps = ['canvas']
