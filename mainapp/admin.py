from django.contrib import admin
from .models import Contact, ArtCategory, ArtObject

# Register your models here.
admin.site.register(ArtCategory)
admin.site.register(ArtObject)
admin.site.register(Contact)
