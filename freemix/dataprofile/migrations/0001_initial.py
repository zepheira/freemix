
from south.db import db
from django.db import models
from freemix.dataprofile.models import *

class Migration:

    def forwards(self, orm):

        # Adding model 'DataProfile'
        db.create_table('dataprofile_dataprofile', (
            ('id', orm['dataprofile.DataProfile:id']),
            ('created', orm['dataprofile.DataProfile:created']),
            ('modified', orm['dataprofile.DataProfile:modified']),
            ('label', orm['dataprofile.DataProfile:label']),
            ('user', orm['dataprofile.DataProfile:user']),
            ('file', orm['dataprofile.DataProfile:file']),
        ))
        db.send_create_signal('dataprofile', ['DataProfile'])

        # Adding model 'DataFile'
        db.create_table('dataprofile_datafile', (
            ('id', orm['dataprofile.DataFile:id']),
            ('created', orm['dataprofile.DataFile:created']),
            ('modified', orm['dataprofile.DataFile:modified']),
            ('name', orm['dataprofile.DataFile:name']),
            ('file', orm['dataprofile.DataFile:file']),
            ('data_profile', orm['dataprofile.DataFile:data_profile']),
        ))
        db.send_create_signal('dataprofile', ['DataFile'])

        # Creating unique_together for [name, data_profile] on DataFile.
        db.create_unique('dataprofile_datafile', ['name', 'data_profile_id'])

        # Creating unique_together for [label, user] on DataProfile.
        db.create_unique('dataprofile_dataprofile', ['label', 'user_id'])



    def backwards(self, orm):

        # Deleting unique_together for [label, user] on DataProfile.
        db.delete_unique('dataprofile_dataprofile', ['label', 'user_id'])

        # Deleting unique_together for [name, data_profile] on DataFile.
        db.delete_unique('dataprofile_datafile', ['name', 'data_profile_id'])

        # Deleting model 'DataProfile'
        db.delete_table('dataprofile_dataprofile')

        # Deleting model 'DataFile'
        db.delete_table('dataprofile_datafile')



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
        'dataprofile.datafile': {
            'Meta': {'unique_together': "(('name', 'data_profile'),)"},
            'created': ('django_extensions.db.fields.CreationDateTimeField', ["_('created')"], {}),
            'data_profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataprofile.DataProfile']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', ["_('modified')"], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'dataprofile.dataprofile': {
            'Meta': {'unique_together': "(('label', 'user'),)"},
            'created': ('django_extensions.db.fields.CreationDateTimeField', ["_('created')"], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.SlugField', [], {'max_length': '200', 'db_index': 'True'}),
            'modified': ('django_extensions.db.fields.ModificationDateTimeField', ["_('modified')"], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['dataprofile']
