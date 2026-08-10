from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import User
from .forms import RechercheForm, ModifierCompteForm

def home(request):
    return render(request, 'app/home.html')

def mon_compte(request):
    return render(
        request,
        'app/mon_compte.html',
        {"user" : request.user}
        )

def modifier_compte(request):
    user = request.user

    if request.method == "POST":
        form = ModifierCompteForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('mon_compte')

    else:
        form = ModifierCompteForm(instance=user)

    return render(
        request,
        'app/modifier_compte.html',
        {'form': form}
    )

def recherche (request):
    form = RechercheForm(request.GET)

    repetiteurs_liste = User.objects.filter(est_prof=True)

    if form.is_valid():
        ville = form.cleaned_data["ville"]
        matiere = form.cleaned_data["matiere"]
        tarif_max = form.cleaned_data["tarif_max"]
        niveau_etudes = form.cleaned_data["niveau_etudes"]

        if ville:
            repetiteurs_liste = repetiteurs_liste.filter(ville=ville)

        if matiere:
            repetiteurs_liste = repetiteurs_liste.filter(sujets_prof=matiere)

        if tarif_max:
            repetiteurs_liste = repetiteurs_liste.filter(tarif__lte=tarif_max)

        if niveau_etudes:
            repetiteurs_liste = repetiteurs_liste.filter(niveau_etudes=niveau_etudes)


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

def demande_lecon (request, user_id):
    prof = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = DemandeLeconForm(request.POST)

        if form.is_valid :
            demande = form.save(commit=False)
            demande.eleve = request.user
            demande.prof = prof
            demande.save()

            return redirect("home")
    
    else :
        form = DemandeLeconForm()

    return render(
        request,
        "app/demande_lecon.html",
        {
            "form": form,
            "prof": prof
        }
    )