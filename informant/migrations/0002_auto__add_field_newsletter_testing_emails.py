# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Newsletter.testing_emails'
        db.add_column('informant_newsletter', 'testing_emails',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Newsletter.testing_emails'
        db.delete_column('informant_newsletter', 'testing_emails')


    models = {
        'informant.newsletter': {
            'Meta': {'ordering': "('date',)", 'object_name': 'Newsletter'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'testing_emails': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
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