from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms.fields import email_re

from petitions.models import Petition

def is_valid_email(email):
    """
    This function checks that the given email address is in-fact valid. It uses the same
    RegExp as used by django.forms to make sure an EmailField is valid.
    
    email -- the email address we need to check
    """
    return True if email_re.match(email) else False
    

class CreatePetitionForm(forms.ModelForm):
    email_list = forms.CharField(widget = forms.Textarea, required = False)

    def clean_email_list(self):
        if self.cleaned_data['email_list'] == "":
            return self.cleaned_data['email_list']
        else:
            for email in self.cleaned_data['email_list'].split(','):
                if not is_valid_email(email.strip()):
                    raise forms.ValidationError(u'Please enter valid email addresses saperated by commas. The faulty email address you submitted was %s.' % email)
            self.cleaned_data['email_list'] = [email.strip() for email in self.cleaned_data['email_list'].split(',')]
            return self.cleaned_data['email_list']

    class Meta:
        model = Petition
        exclude = ('creator', 'datetime_created', 'slug_name')
