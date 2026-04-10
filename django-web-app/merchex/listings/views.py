from django.shortcuts import render
from django.shortcuts import redirect
from django.core.mail import send_mail

from django.http import HttpResponse

from listings.models import Band, Listings
from listings.forms import BandForm, ListingForm, ContactUsForm

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

def band_create(request):
    form = BandForm()
    if request.method == 'POST' :
        form = BandForm(request.POST)
        if form.is_valid :
            band=form.save()
            return redirect('band-detail', band.id)
    
    else : 
        form = BandForm()

    return render(request,
            'listings/bands_create.html',
            {'form': form})

def band_change (request, id):
    band = Band.objects.get(id=id)

    if request.method == 'POST' :
        form = BandForm(request.POST, instance=band)

        if form.is_valid():
            form.save()
            return redirect('band-detail', band.id)
    
    else:
        form = BandForm(instance=band)

    return render(request, 'listings/bands_change.html', {'form': form })

def band_delete (request, id):
        band=Band.objects.get(id=id)

        if request.method == 'POST':
            band.delete()
            return redirect('band-list')
        else:
            return render(request, 'listings/bands_delete.html', {'band' : band })

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

def listing_create (request):
    form = ListingForm()

    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid() :
            listing = form.save()
            return redirect ('listing-detail', listing.id)
        
    else :
        form = ListingForm()   

    return render(request, 'listings/listings_create.html', {'form' : form})

def listing_change (request, id):
    listing=Listings.objects.get(id=id)

    if request.method == 'POST':
        form=ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect ('listing-detail',listing.id)
    else :
        form=ListingForm(instance=listing)   

    return render(request,'listings/listing_change.html', {'form':form}) 

def listing_delete (request, id):
        listing=Listings.objects.get(id=id)
        if request.method == 'POST':
            listing.delete()
            return redirect('listing-list')
        else:
            return render(request, 'listings/bands_delete.html', {'listing' : listing })

def contact (request) :
    form = ContactUsForm()
    
    if request.method == 'POST' :
        form = ContactUsForm(request.POST)
        
        if form.is_valid() :
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via MerchEx Contact Us form',                message = form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@merchex.xyz'],
                )
            return redirect('email-sent') 

    else :
        form = ContactUsForm()
    
    return render(request, 'listings/contact.html', {'form':form})

def email_sent (request):
    return render(request, 'listings/email_sent.html')