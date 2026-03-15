from django.shortcuts import render

from django.http import HttpResponse

from listings.models import Band

def hello(request):
    bands = Band.objects.all()
    return render(request,'listings/hello.html',{'bands': bands})

def about(request):
    return render(request,'listings/about.html')