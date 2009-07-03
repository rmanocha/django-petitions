
from south.db import db
from django.db import models
from django.template import defaultfilters
from petitions.models import *

class Migration:
    
    def forwards(self, orm):
        "Write your forwards migration here"
        for petition in orm.Petition.objects.all():
            petition.slug_name = defaultfilters.slugify(petition.title)
            petition.save()
    
    
    def backwards(self, orm):
        "Write your backwards migration here"
        for petition in orm.Petition.objects.all():
            petition.slug_name = None
            petition.save()
    
    
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
            'slug_name': ('models.SlugField', [], {'max_length': '200', 'null': 'True', 'unique': 'True'}),
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
