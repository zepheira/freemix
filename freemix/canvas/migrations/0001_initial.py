
from south.db import db
from django.db import models
from freemix.canvas.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'Canvas'
        db.create_table('canvas_canvas', (
            ('id', orm['canvas.Canvas:id']),
            ('slug', orm['canvas.Canvas:slug']),
            ('name', orm['canvas.Canvas:name']),
            ('description', orm['canvas.Canvas:description']),
            ('location', orm['canvas.Canvas:location']),
        ))
        db.send_create_signal('canvas', ['Canvas'])



    def backwards(self, orm):

        # Deleting model 'Canvas'
        db.delete_table('canvas_canvas')



    models = {
        'canvas.canvas': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Label'", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['canvas']
