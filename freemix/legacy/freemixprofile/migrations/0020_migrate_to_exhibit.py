# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for fp in orm["freemixprofile.Freemix"].objects.all():
            canvas = orm["exhibit.Canvas"].objects.get(id=fp.canvas.id)
            theme = orm["exhibit.Theme"].objects.get(id=fp.theme.id)

            e = orm["exhibit.Exhibit"](
                canvas = canvas,
                created=fp.created,
                dataset = fp.dataset,
                description = fp.description,
                modified = fp.modified,
                owner = fp.user,
                profile = fp.json,
                published=True,
                slug = fp.slug,
                theme = theme,
                title = fp.title
            ).save()

    def backwards(self, orm):
        for fp in orm["exhibit.Exhibit"].objects.all():
            canvas = orm["canvas.Canvas"].objects.get(id=fp.canvas.id)
            theme = orm["freemixprofile.ExhibitTheme"].objects.get(id=fp.theme.id)

            e = orm["freemixprofile.Freemix"](
                canvas = canvas,
                created=fp.created,
                dataset = fp.dataset,
                description = fp.description,
                modified = fp.modified,
                user = fp.owner,
                json = fp.slug,
                slug = fp.slug,
                theme = theme,
                title = fp.title
            ).save()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'canvas.canvas': {
            'Meta': {'object_name': 'Canvas'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Label'", 'max_length': '30'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'dataset.dataset': {
            'Meta': {'ordering': "('-modified',)", 'unique_together': "(('slug', 'owner'),)", 'object_name': 'Dataset'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': '\'{"items": []}\''}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'datasets'", 'null': 'True', 'to': "orm['auth.User']"}),
            'profile': ('django.db.models.fields.TextField', [], {'default': '\'{"properties": []}\''}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'datasets'", 'null': 'True', 'to': "orm['dataset.DataSource']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'dataset.datasource': {
            'Meta': {'object_name': 'DataSource'},
            'classname': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'data_sources'", 'null': 'True', 'to': "orm['auth.User']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'})
        },
        'exhibit.canvas': {
            'Meta': {'object_name': 'Canvas'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'exhibit.exhibit': {
            'Meta': {'ordering': "('-modified',)", 'unique_together': "(('slug', 'owner'),)", 'object_name': 'Exhibit'},
            'canvas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibit.Canvas']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exhibits'", 'to': "orm['dataset.Dataset']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'exhibits'", 'null': 'True', 'to': "orm['auth.User']"}),
            'profile': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['exhibit.Theme']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'exhibit.theme': {
            'Meta': {'object_name': 'Theme'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'static/images/thumbnails/three-column/smoothness.png'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "'/static/exhibit/css/smoothness/smoothness.css'", 'max_length': '100'})
        },
        'freemixprofile.exhibittheme': {
            'Meta': {'object_name': 'ExhibitTheme'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "'static/images/thumbnails/three-column/smoothness.png'", 'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'default': "'/static/view_theme/smoothness/smoothness.css'", 'max_length': '100'})
        },
        'freemixprofile.freemix': {
            'Meta': {'ordering': "('-modified',)", 'unique_together': "(('slug', 'user'),)", 'object_name': 'Freemix'},
            'canvas': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['canvas.Canvas']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dataset.Dataset']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'json': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['freemixprofile.ExhibitTheme']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }

    complete_apps = ['exhibit', 'freemixprofile']
