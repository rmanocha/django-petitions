
from south.db import db
from django.db import models
from petitions.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Petition.title'
        db.alter_column('petitions_petition', 'title', models.CharField(unique=True, max_length=200))
        
    
    
    def backwards(self, orm):
        
        # Changing field 'Petition.title'
        db.alter_column('petitions_petition', 'title', models.CharField(max_length=200))
        
    
    
    models = {
        'petitions.petitionsignature': {
            'Meta': {'ordering': "['datetime_signed']", 'unique_together': "('petition','signator')"},
            'comment': ('models.TextField', [], {'blank': 'True'}),
            'datetime_signed': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'petition': ('models.ForeignKey', ["orm['petitions.Petition']"], {}),
            'signator': ('models.ForeignKey', ["orm['auth.User']"], {})
        },
        'petitions.petition': {
            'creator': ('models.ForeignKey', ["orm['auth.User']"], {}),
            'datetime_created': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'text': ('models.TextField', [], {}),
            'title': ('models.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label','model'),)", 'db_table': "'django_content_type'"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'petitions.petitionrelatedobject': {
            'content_type': ('models.ForeignKey', ["orm['contenttypes.ContentType']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('models.IntegerField', [], {}),
            'petition': ('models.ForeignKey', ["orm['petitions.Petition']"], {})
        }
    }
    
    complete_apps = ['petitions']
