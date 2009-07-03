from django import forms

from petitions.models import Petition

class CreatePetitionForm(forms.ModelForm):
    class Meta:
        model = Petition
        exclude = ('creator', 'datetime_created', 'slug_name')
