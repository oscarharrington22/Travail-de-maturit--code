from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import User
from .forms import RechercheForm

def home(request):
    return render(request, 'app/home.html')

def recherche (request):
    form = RechercheForm(request.GET)

    repetiteurs_liste = User.objects.filter(est_prof=True)

    ville = request.GET.get('ville')
    matiere = request.GET.get('matiere')
    tarif_max = request.GET.get('tarif_max')
    

    if ville :
        repetiteurs_liste = repetiteurs_liste.filter(ville=ville)

    if matiere :
        repetiteurs_liste = repetiteurs_liste.filter(sujets_prof=matiere)
    
    if tarif_max :
        repetiteurs_liste = repetiteurs_liste.filter(tarif__lte= tarif_max)

    return render(
        request,
        'app/recherche.html',
        {   
        'form': form,
        'repetiteurs_liste': repetiteurs_liste
            }
    )

def profil (request, user_id):
    repetiteur = User.objects.get(id=user_id)

    return render(request, "app/profil.html", {"repetiteur": repetiteur})