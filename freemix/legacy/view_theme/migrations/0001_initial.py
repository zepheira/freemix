
from south.db import db
from django.db import models

class Migration:

    def forwards(self, orm):

        # Adding model 'Theme'
        db.create_table('view_theme_theme', (
            ('id', orm['view_theme.Theme:id']),
            ('slug', orm['view_theme.Theme:slug']),
            ('name', orm['view_theme.Theme:name']),
            ('description', orm['view_theme.Theme:description']),
            ('url', orm['view_theme.Theme:url']),
            ('thumbnail', orm['view_theme.Theme:thumbnail']),
            ('enabled', orm['view_theme.Theme:enabled']),
        ))
        db.send_create_signal('view_theme', ['Theme'])



    def backwards(self, orm):

        # Deleting model 'Theme'
        db.delete_table('view_theme_theme')



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
