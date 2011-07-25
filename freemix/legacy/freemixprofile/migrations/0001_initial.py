
from south.db import db
from django.db import models
from freemix.legacy.freemixprofile.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'Freemix'
        db.create_table('freemixprofile_freemix', (
            ('id', orm['freemixprofile.Freemix:id']),
            ('created', orm['freemixprofile.Freemix:created']),
            ('modified', orm['freemixprofile.Freemix:modified']),
            ('label', orm['freemixprofile.Freemix:label']),
            ('user', orm['freemixprofile.Freemix:user']),
            ('file', orm['freemixprofile.Freemix:file']),
            ('data_profile', orm['freemixprofile.Freemix:data_profile']),
        ))
        db.send_create_signal('freemixprofile', ['Freemix'])

        # Creating unique_together for [label, user] on Freemix.
        db.create_unique('freemixprofile_freemix', ['label', 'user_id'])



    def backwards(self, orm):

        # Deleting unique_together for [label, user] on Freemix.
        db.delete_unique('freemixprofile_freemix', ['label', 'user_id'])

        # Deleting model 'Freemix'
        db.delete_table('freemixprofile_freemix')



    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
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
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dataprofile.dataprofile': {
            'Meta': {'unique_together': "(('label', 'user'),)"},
            'created': ('django_extensions.db.fields.CreationDateTimeField', ["_('created')"], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', ["_('modified')"], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'freemixprofile.freemix': {
            'Meta': {'unique_together': "(('label', 'user'),)"},
            'created': ('django_extensions.db.fields.CreationDateTimeField', ["_('created')"], {}),
            'data_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataprofile.DataProfile']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', ["_('modified')"], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['freemixprofile']
