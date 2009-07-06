How to use django-petitions
------------------------------

``django-petitions`` allows for basic petitions functionality in your django project.
It is in use on GovCheck.net (http://govcheck.net) at http://govcheck.net/petitions/.
``django-petitions`` is released under the BSD license. See License.txt for more
details.

### Install

For now, to install django-petitions, check it out from github using:

        git clone git://github.com/rmanocha/django-petitions.git

You can then copy either copy the petitions folder to your python distribution's
``site-packages`` folder or create a symbolic link.

### Adding ``django-petitions`` to your project

You will need to add the petitions app to your ``INSTALLED_APPS`` setting in 
your settings.py file. It should look something like::

        INSTALLED_APPS = (
            # ...
            'petitions',
        )

You will now need to create the required tables. To do this, run the following
command from your project's root folder::

        python manage.py syncdb

You will also need to add the petitions urls to your site's URLConf. You can 
do this by adding the following line to your URLConf::

        (r'petitions/', include('petitions.urls')),

That's it. You can now create petitions by going to ``/petitions/add/`` and 
view a complete list of create petitions at ``/petitions/``.

Notes on ``views.py``
---------------------

There are 3 views defined in ``django-petitions``.

1. ``create_new_petition``
    
    This view is used to display and process the form used to create
    new petitions. By default, the form used to create new petitions is
    CreatePetitionForm defined in ``forms.py``. However, you might want 
    to define a custom form with additional fields. You can do this by 
    sending in a custom form class to the view from your URLConf like so::

    url(r'petitions/add/$', 'petitions.views.create_new_petition', {'form_class' : FullCreatePetitionForm}, name = 'create-new-petition'),

    The default template used to display the form is ``petitions/new_petition.html``.
    This too can be changed by passing in the ``template_name`` arg to the
    ``create_new_petition`` view (same as with the custom form).

    This view sends out a custom signal (defined in ``signals.py``) called
    ``petition_saved`` with the bound form and the newly created petition as
    arguments. You can connect to this signal to do any sort of post-processing (
    such as sending out emails to alert people of a new petition being created etc.)

2. ``sign_petition``

    This view is used to allow users to sign a given petition. It creates 
    PetitionSignature objects. This view requires you to make a POST AJAX request
    with the petition id (as ``petition_id``) and comments (as ``sign_comment``)
    as arguments. If the request is not made via an AJAX call, a HTTP 404 error is
    thrown.

3. ``get_petition_signators``

    This view is used to get details about the signatures for a given petition.
    It requires you to make a GET AJAX call with the ``petition_id`` defined. 
    In addition is also needs a ``data`` argument which should be either of 
    ``full`` or ``count``. See the docs in the function signature to understand
    what each does.

Notes on ``migrations``
-----------------------

Any changes in the models are done using south (http://south.aeracode.org/). If you 
have already installed the app and see some additional features that will need changing
the models, you will need to run the relevant migrations. Read south's website to learn
how to do that.
