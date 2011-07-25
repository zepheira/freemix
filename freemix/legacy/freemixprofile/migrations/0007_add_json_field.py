# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Freemix.json'
        db.add_column('freemixprofile_freemix', 'json', self.gf('django_extensions.db.fields.json.JSONField')(default='{}'), keep_default=False)

        # Changing field 'Freemix.created'
        db.alter_column('freemixprofile_freemix', 'created', self.gf('django.db.models.fields.DateTimeField')(blank=True))

        # Changing field 'Freemix.modified'
        db.alter_column('freemixprofile_freemix', 'modified', self.gf('django.db.models.fields.DateTimeField')(blank=True))

    def backwards(self, orm):
        
        # Deleting field 'Freemix.json'
        db.delete_column('freemixprofile_freemix', 'json')

        # Changing field 'Freemix.created'
        db.alter_column('freemixprofile_freemix', 'created', self.gf('django_extensions.db.fields.CreationDateTimeField')(blank=True))

        # Changing field 'Freemix.modified'
        db.alter_column('freemixprofile_freemix', 'modified', self.gf('django_extensions.db.fields.ModificationDateTimeField')(blank=True))


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'canvas.canvas': {
            'Meta': {'object_name': 'Canvas'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Label'", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'static/images/thumbnails/three-column/smoothness.png'", 'max_length': '100'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dataprofile.dataprofile': {
            'Meta': {'unique_together': "(('slug', 'user'),)", 'object_name': 'DataProfile'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data_sets'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'freemixprofile.freemix': {
            'Meta': {'unique_together': "(('slug', 'user'),)", 'object_name': 'Freemix'},
            'canvas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['canvas.Canvas']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'data_profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data_views'", 'to': "orm['dataprofile.DataProfile']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django_extensions.db.fields.json.JSONField', [], {'default': "'{}'"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['view_theme.Theme']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data_views'", 'null': 'True', 'to': "orm['auth.User']"})
        },
        'view_theme.theme': {
            'Meta': {'object_name': 'Theme'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Label'", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'static/images/thumbnails/three-column/smoothness.png'", 'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "'/site_media/static/view_theme/smoothness/smoothness.css'", 'max_length': '100'})
        }
    }

    complete_apps = ['freemixprofile']
