from django.contrib import admin
from listings.models import Band , Listings

class BandAdmin (admin.ModelAdmin) :
    list_display = ('name', 'year_formed', 'genre')

admin.site.register(Band, BandAdmin)

class ListingsAdmin (admin.ModelAdmin) :
    list_display = ('title', 'band')

admin.site.register(Listings)