from django.contrib import admin
from petitions.models import Petition, PetitionSignature

class PetitionAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime_created'
    list_display = ('title', 'creator', 'datetime_created')

admin.site.register(Petition, PetitionAdmin)

class PetitionSignatureAdmin(admin.ModelAdmin):
    date_hierarchy = 'datetime_signed'
    list_display = ('petition', 'signator', 'datetime_signed')

admin.site.register(PetitionSignature, PetitionSignatureAdmin)
