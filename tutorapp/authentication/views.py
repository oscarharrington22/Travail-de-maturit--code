from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Disponibilite
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

@login_required
def mes_disponibilites(request):
    disponibilites_liste = request.user.disponibilites.all()
    if not request.user.est_prof:
        return redirect('home')

    return render(request, 'authentication/mes_disponibilites.html',{'disponibilites_liste': disponibilites_liste})

@login_required
def nouvelle_disponibilite(request):
    if request.method == 'POST':
        form = DisponibiliteForm(request.POST)
        if form.is_valid():
            creneau = form.save(commit=False)
            creneau.prof = request.user
            creneau.save()
            return redirect('mes_disponibilites')
        
    else:
        form = DisponibiliteForm()
    
    return render(request, 'authentication/nouvelle_disponibilite.html', {'form' : form})

@login_required
def supprimer_disponibilite(request, id):
    creneau = Disponibilite.objects.get(id=id, prof=request.user)
    creneau.delete()
    return redirect('mes_disponibilites')