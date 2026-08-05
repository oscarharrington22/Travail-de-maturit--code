from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from authentication.models import User
from .forms import Recherche

@login_required
def home(request):
    return render(request, 'app/home.html')

def recherche (request):
    form = RechercheForm(request.GET)

    repetiteurs = User.objects.filter(est_prof=True)

    ville = request.GET.get('ville')
    matiere = request.GET.get('matiere')
    tarif_max = request.GET.get('tarif_max')
    

    if ville :
        repetiteurs = repetiteurs.filter(ville=ville)

    if matiere :
        repetiteurs = repetiteurs.filter(sujets_prof=matiere)
    
    if tarif_max :
        repetiteurs = repetiteurs.filter(tarif__lte= tarif_max)

    return render(
        request,
        'app/recherche.html',
        {   
        'form': form,
        'repetiteurs': repetiteurs
            }
    )