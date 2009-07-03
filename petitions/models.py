from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

class Petition(models.Model):
    title = models.CharField(verbose_name='Title of this petition', max_length=200, unique = True)
    slug_name = models.SlugField(verbose_name = 'Petition\'s slug name', unique = True, null = True, max_length = 200)
    text = models.TextField(verbose_name='Text of this petition')
    creator = models.ForeignKey(User, verbose_name='The creator of this petition')
    datetime_created = models.DateTimeField(verbose_name='Date and Time when this petition was created', auto_now_add = True)

    def get_absolute_url(self):
        return reverse('petition-details', args = [self.slug_name])

    def __unicode__(self):
        return '%s (%s)' % (self.title, self.creator)

    class Meta:
        ordering = ['datetime_created']

class PetitionRelatedObject(models.Model):
    petition = models.ForeignKey(Petition, verbose_name='The associated petition')
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    related_object = generic.GenericForeignKey()

    def __unicode__(self):
        return '%s' % self.petition

class PetitionSignature(models.Model):
    petition = models.ForeignKey(Petition, verbose_name='The associated petition')
    signator = models.ForeignKey(User, verbose_name='The user who signed the petition')
    datetime_signed = models.DateTimeField(verbose_name='Date and time when this user signed this petition', auto_now_add = True)
    comment = models.TextField(verbose_name='Comments made by signator', blank = True)

    def __unicode__(self):
        return '%s signed by %s on %s' % (self.petition, self.signator, str(self.datetime_signed))

    class Meta:
        unique_together = ('petition', 'signator')
        ordering = ['datetime_signed']

def petition_post_save_callback(sender, **kwargs):
    """
    This listener exists so that we can create a slug for every new petition.
    We check if a slug exists for the given petition. If it doesn't, we 
    use django.template.defaultfilters.slugify to create a slug from the title.
    If the generated slug exists in the DB, then we join in the petition's id 
    into the slug and save the petition, else we just use the slug create from
    the title as the object's slug_name
    """
    if sender == Petition:
        petition = kwargs.pop('instance')
        created = kwargs.pop('created')

        if created:
            if not petition.slug_name:
                slug = slugify(petition.title)
                if sender.objects.filter(slug_name = slug).count() or slug in ('add', 'sign-petition', 'petition-signators'):
                    petition.slug_name = '-'.join([slug, unicode(petition.id)])
                    petition.save()
                else:
                    petition.slug_name = slug
                    petition.save()
    
models.signals.post_save.connect(petition_post_save_callback)

