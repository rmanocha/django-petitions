from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.fields import email_re

from petitions.models import Petition

class CreatePetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        exclude = ('creator', 'datetime_created', 'slug_name')
