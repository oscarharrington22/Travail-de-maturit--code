from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import User, Disponibilite

from authentication.forms import SignupProfForm
from .forms import RechercheForm, ModifierCompteForm, DemandeLeconForm, StatutDemandeForm
from app.models import DemandeLecon

@login_required
def home(request):
    return render(request, 'app/home.html')

@login_required
def mon_compte(request):
    return render(
        request,
        'app/mon_compte.html',
        {"user" : request.user}
        )

@login_required
def modifier_compte(request):
    user = request.user

    if request.method == "POST":
        form = ModifierCompteForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            if user.est_prof:
                return redirect('modifier_compte_prof')
            return redirect('mon_compte')

    else:
        form = ModifierCompteForm(instance=user)

    return render(
        request,
        'app/modifier_compte.html',
        {'form': form}
    )

@login_required
def modifier_compte_prof(request):
    user = request.user

    if request.method == "POST":
        form =SignupProfForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('mon_compte')

    else:
        form = SignupProfForm(instance=user)

    return render(
        request,
        'app/modifier_compte.html',
        {'form': form}
    )

@login_required
def recherche (request):
    form = RechercheForm(request.GET)

    repetiteurs_liste = User.objects.filter(est_prof=True)

    if form.is_valid():
        ville = form.cleaned_data["ville"]
        matiere = form.cleaned_data["matiere"]
        tarif_max = form.cleaned_data["tarif_max"]
        niveau_etudes = form.cleaned_data["niveau_etudes"]
        jour = form.cleaned_data['jour']
        heure = form.cleaned_data['heure']

        if request.user.est_prof:
            repetiteurs_liste = repetiteurs_liste.exclude(id=request.user.id)
        
        if ville:
            repetiteurs_liste = repetiteurs_liste.filter(ville=ville)

        if matiere:
            repetiteurs_liste = repetiteurs_liste.filter(sujets_prof=matiere)

        if tarif_max:
            repetiteurs_liste = repetiteurs_liste.filter(tarif__lte=tarif_max)

        if niveau_etudes:
            repetiteurs_liste = repetiteurs_liste.filter(niveau_etudes=niveau_etudes)

        if jour:
            repetiteurs_liste = repetiteurs_liste.filter(disponibilites__jour=jour)

        if heure:
            repetiteurs_liste = repetiteurs_liste.filter(disponibilites__heure_debut__lte=heure, disponibilites__heure_fin__gte=heure)

    return render(
        request,
        'app/recherche.html',
        {   
        'form': form,
        'repetiteurs_liste': repetiteurs_liste
            }
    )

@login_required
def profil (request, user_id):
    repetiteur = User.objects.get(id=user_id)
    disponibilite_liste = Disponibilite.objects.filter(prof=repetiteur)

    return render(request, "app/profil.html", 
        {
        "repetiteur": repetiteur,
         "disponibilite_liste": disponibilite_liste
         }
    )

@login_required
def demande_lecon (request, user_id):
    prof = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = DemandeLeconForm(request.POST)
        if form.is_valid ():
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

@login_required
def mes_demandes_envoyees (request) :
    demandes_liste = request.user.demandes_comme_eleve.all()

    return render (request, 'app/mes_demandes.html', {'demandes_liste' : demandes_liste})

@login_required
def mes_demandes_recues (request) : 
    demandes_liste = request.user.demandes_comme_prof.all()

    return render (request, 'app/mes_demandes.html', {'demandes_liste' : demandes_liste})

@login_required
def repondre_demande(request, demande_id):
    demande = DemandeLecon.objects.get(id=demande_id)

    if demande.prof != request.user:
        return redirect("mes_demandes_recues")

    if request.method == 'POST':
        form = StatutDemandeForm(request.POST, instance=demande)

        if form.is_valid():
            form.save()
            return redirect("mes_demandes_recues")

    else:
        form = StatutDemandeForm(instance=demande)

    return render(
        request,
        "app/repondre_demande.html",
        {"form": form, "demande": demande}
    )

@login_required
def supprimer_demande(request, demande_id):
    demande = DemandeLecon.objects.get(id=demande_id)

    if demande.eleve != request.user and demande.prof != request.user:
        return redirect("mes_demandes_envoyees")

    demande.delete()

    return redirect("mes_demandes_envoyees")