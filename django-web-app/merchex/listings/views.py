from django.shortcuts import render

from django.http import HttpResponse

from listings.models import Band, Listings

def about(request):
    return render(request,'listings/about.html')

def band_list(request):
    bands = Band.objects.all()
    return render(request,
            'listings/band_list.html', 
            {'bands': bands})

def band_detail(request, id):
    band=Band.objects.get(id=id)
    return render(request,
          'listings/band_detail.html',
          {'band': band})

def listing_list(request):
    listing=Listings.objects.all()
    return render(request, 
            'listings/listings_list.html',
            {'listing' : listing})

def listing_detail (request, id) :
    listing = Listings.objects.get(id=id)
    return render (request, 
            'listings/listings_detail.html', 
            {'listing' : listing})