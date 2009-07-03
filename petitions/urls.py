from django.conf.urls.defaults import *

from petitions.models import Petition

urlpatterns = patterns('petitions.views',
    url(r'^add/$',                              'create_new_petition', name = 'create-new-petition'),
    url(r'^sign-petition/$',                    'sign_petition', name = 'sign-petition'),
    url(r'^petition-signators/$',               'get_petition_signators', name = 'petition-signators'),
)

urlpatterns += patterns('django.views.generic',
    url(r'^$',                                  'list_detail.object_list', {'queryset' : Petition.objects.all().select_related(), 'template_name' : 'petitions/list_petitions.html'}, name = 'show-all-petitions'),
    url(r'^(?P<slug>[\-\d\w]+)/$',              'list_detail.object_detail', {'queryset' : Petition.objects.all(), 'template_name' : 'petitions/petition_detail.html', 'slug_field' : 'slug_name'}, name = 'petition-details'),
    url(r'^(?P<slug>[\-\d\w]+)/comments/$',     'list_detail.object_detail', {'queryset' : Petition.objects.all(), 'template_name' : 'petitions/petition_comments.html', 'slug_field' : 'slug_name'}, name = 'petition-comments'),
)

