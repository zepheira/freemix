# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    depends_on=(
        ('freemixprofile', '0013_drop_freemix_view_theme',),
    )
    def forwards(self, orm):

        # Deleting model 'theme'
        db.delete_table('view_theme_theme')


    def backwards(self, orm):

        # Adding model 'theme'
        db.create_table('view_theme_theme', (
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(default='/site_media/static/view_theme/smoothness/smoothness.css', max_length=100)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='static/images/thumbnails/three-column/smoothness.png', max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Label', max_length=30)),
        ))
        db.send_create_signal('view_theme', ['theme'])


    models = {

    }

    complete_apps = ['view_theme']
