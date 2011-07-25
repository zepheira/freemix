# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Canvas.thumbnail'
        db.alter_column('canvas_canvas', 'thumbnail', self.gf('django.db.models.fields.URLField')(max_length=200))


    def backwards(self, orm):
        
        # Changing field 'Canvas.thumbnail'
        db.alter_column('canvas_canvas', 'thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100))


    models = {
        'canvas.canvas': {
            'Meta': {'object_name': 'Canvas'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Label'", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['canvas']
