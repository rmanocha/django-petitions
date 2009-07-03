
from south.db import db
from django.db import models
from petitions.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'PetitionSignature'
        db.create_table('petitions_petitionsignature', (
            ('id', models.AutoField(primary_key=True)),
            ('petition', models.ForeignKey(orm.Petition)),
            ('signator', models.ForeignKey(orm['auth.User'])),
            ('datetime_signed', models.DateTimeField(auto_now_add=True)),
            ('comment', models.TextField(blank=True)),
        ))
        db.send_create_signal('petitions', ['PetitionSignature'])
        
        # Adding model 'Petition'
        db.create_table('petitions_petition', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=200)),
            ('text', models.TextField()),
            ('creator', models.ForeignKey(orm['auth.User'])),
            ('datetime_created', models.DateTimeField(auto_now_add=True)),
        ))
        db.send_create_signal('petitions', ['Petition'])
        
        # Adding model 'PetitionRelatedObject'
        db.create_table('petitions_petitionrelatedobject', (
            ('id', models.AutoField(primary_key=True)),
            ('petition', models.ForeignKey(orm.Petition)),
            ('content_type', models.ForeignKey(orm['contenttypes.ContentType'])),
            ('object_id', models.IntegerField()),
        ))
        db.send_create_signal('petitions', ['PetitionRelatedObject'])
        
        # Creating unique_together for [petition, signator] on PetitionSignature.
        db.create_unique('petitions_petitionsignature', ['petition_id', 'signator_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'PetitionSignature'
        db.delete_table('petitions_petitionsignature')
        
        # Deleting model 'Petition'
        db.delete_table('petitions_petition')
        
        # Deleting model 'PetitionRelatedObject'
        db.delete_table('petitions_petitionrelatedobject')
        
        # Deleting unique_together for [petition, signator] on PetitionSignature.
        db.delete_unique('petitions_petitionsignature', ['petition_id', 'signator_id'])
        
    
    
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
            'title': ('models.CharField', [], {'max_length': '200'})
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
