# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Newsletter'
        db.create_table('informant_newsletter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('informant', ['Newsletter'])

        # Adding model 'Recipient'
        db.create_table('informant_recipient', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('md5', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('informant', ['Recipient'])


    def backwards(self, orm):
        # Deleting model 'Newsletter'
        db.delete_table('informant_newsletter')

        # Deleting model 'Recipient'
        db.delete_table('informant_recipient')


    models = {
        'informant.newsletter': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Newsletter'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'informant.recipient': {
            'Meta': {'ordering': "('email',)", 'object_name': 'Recipient'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'md5': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['informant']