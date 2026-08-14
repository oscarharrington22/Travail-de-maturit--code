from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from authentication.forms import DisponibiliteForm

from . import forms

def logout_user(request):
    logout(request)
    return redirect('login')

def signup_page(request):
    form = forms.SignupForm()

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})

def mes_disponibilites(request):
    disponibilites_liste = request.user.disponibilites.all()

    return render(request, 'mes_disponibilites.html',{'disponibilites_liste': disponibilites_liste})

def nouvelle_disponibilite(request, user_id):
    if request.method == 'POST':
        form = DisponibiliteForm(request.POST)
        if form.is_valid:
            creneau = form.save(commit=False)
            creneau.prof = request.user
            creneau.save()
            return redirect('mes_disponibilites')
        
    else:
        form = DisponibiliteForm()
    
    return render(request, 'nouvelle_disponibilite.html', {'form' : form})