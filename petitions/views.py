from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.core.urlresolvers import reverse

from petitions.models import Petition, PetitionSignature
from petitions.forms import CreatePetitionForm
from petitions.signals import petition_saved

@login_required
def create_new_petition(request, form_class = CreatePetitionForm,
            template_name = 'petitions/new_petition.html'):
    """
    This view will allow users to create a new petition.
    A User needs to be logged in to create a new petition.
    
    request -- the Request object
    form_class -- The Form Class to use for creating a new Petition
    template_name -- A custom template to use to display the petition creation form
    """
    if request.POST:
        petition_form = form_class(request.POST)
        if petition_form.is_valid():
            petition = petition_form.save(commit = False)
            petition.creator = request.user
            petition.save()

            petition_saved.send(sender = Petition, petition_form = petition_form, petition = petition)

            return HttpResponseRedirect(reverse('petition-details', args = [petition.slug_name]))
    else:
        petition_form = form_class()
    return render_to_response(template_name, {'petition_form' : petition_form})

@login_required
def sign_petition(request):
    """
    This view will allow a user to sign a given petition.

    The data should be sent via a POST AJAX request containing a 'petition_id'
    for which this petition is being signed and 'sign_comment' which is the comments
    the user added when signing the petition. Of-course, the user needs to be logged in.
    Raises a 404 error if any of the above is not true.
    
    request -- the Request object
    """
    if request.is_ajax() and request.POST.get('petition_id') and request.POST.get('sign_comment'):
        petition_id = int(request.POST.get('petition_id'))
        PetitionSignature.objects.create(petition = Petition.objects.get(pk = petition_id), signator = request.user, comment = request.POST.get('sign_comment').strip())
        return HttpResponse('success')
    else:
        #Need to figure out if I should throw a 500 or 404 error here.
        raise Http404

def get_petition_signators(request):
    """
    This view will return a json encoded string listing
    out the users who have signed the given petition (as 
    indicated by petition_id). The request needs to be made via a GET AJAX
    request. Two additional options exist. You can request for all the signature
    data for the given petition or just the count of the no. of signatures for the
    given petition. This is indicated by passing 'full' or 'count' to the 'data'
    key in the request.

    Throws a 404 error if the request is not made via an AJAX call or if 'data' is
    not one of 'full' or 'count'
    
    request -- the Request object
    """
    if request.is_ajax():
        petition_id = int(request.GET.get('petition_id',0))
        datatype = request.GET.get('data', None)
        if (petition_id <= 0) or (datatype not in ('full','count')):
            raise Http404
        if datatype == 'full':
            petition_signators = [petition_signature.signator for petition_signature in PetitionSignature.objects.filter(petition__id = petition_id).select_related('signator')]
            data = {'user_has_signed' : False, 'signators' : [' '.join([signator.first_name, signator.last_name]) for signator in petition_signators]}
            if request.user.username:
                if request.user in petition_signators:
                    data['user_has_signed'] = True
        else:
            data = {'user_has_signed' : False, 'count' : PetitionSignature.objects.filter(petition__id = petition_id).count()}
            if request.user.username:
                if PetitionSignature.objects.filter(petition__id = petition_id, signator = request.user).count() == 1:
                    data['user_has_signed'] = True

        return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    else:
        raise Http404
    
