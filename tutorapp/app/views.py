from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import User, Disponibilite

from authentication.forms import SignupProfForm
from .forms import RechercheForm, ModifierCompteForm, DemandeLeconForm, StatutDemandeForm
from app.models import DemandeLecon

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
def page_modification(request):
    return render(request, 'app/page_modification.html')

@login_required
def modifier_compte(request):
    user = request.user

    if request.method == "POST":
        form = ModifierCompteForm(request.POST, instance=user)
        #instance=user rempli le formulaire avec les donnée de l'instance user 
        #ça permet de modifier les données déjà existantes

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
#deuxième formulaire d'incription qui sera appelé seulement si l'utilisateur coche qu'il est prof


def recherche (request):
    form = RechercheForm(request.GET)

    repetiteurs_liste = User.objects.filter(est_prof=True)
    #Prend tous les utilisateurs listés comme répétiteurs
    #Cette liste va être filtrée puis envoyée au gabarit pour être affichée

    if form.is_valid():
        last_name = form.cleaned_data["last_name"]
        ville = form.cleaned_data["ville"]
        matiere = form.cleaned_data["matiere"]
        tarif_max = form.cleaned_data["tarif_max"]
        niveau_etudes = form.cleaned_data["niveau_etudes"]
        jour = form.cleaned_data['jour']
        heure = form.cleaned_data['heure']
        #cleaned_data récupère la valeur du champ indiqué pour pouvoir l'utiliser dans les filtres plus bas

        if request.user.is_authenticated and request.user.est_prof:
            repetiteurs_liste = repetiteurs_liste.exclude(id=request.user.id)
            #exclude permet d'exculre l'utilisateur de la liste 

        if last_name:
            repetiteurs_liste = repetiteurs_liste.filter(last_name=last_name)

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
            #les 2 '__' indiquent qu'il faut aller checher le champ jour dans le modèle disponibilites 

        if heure:
            repetiteurs_liste = repetiteurs_liste.filter(disponibilites__heure_debut__lte=heure, disponibilites__heure_fin__gte=heure)
            #lte signifie less then or equal (<=) et gte greater then or equal (>=)

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

            jours = [
                "lundi",
                "mardi",
                "mercredi",
                "jeudi",
                "vendredi",
                "samedi",
                "dimanche"
            ]
            #Liste de jours pour pouvoir utiliser l'indexe de .weekday
            
            jour = jours[demande.date.weekday()]

            disponibilite = Disponibilite.objects.filter(
                prof=prof,
                jour=jour,
                heure_debut__lte=demande.heure_debut,
                heure_fin__gte=demande.heure_fin
                ).exists()
            #Vérifie s'il existe (fonction .exists()) une disponibilité à cette date entre les heures de disponibilité

            if disponibilite:
                demande.save()
                return redirect("home")

            else:
                form.add_error(
                    None,
                    "Le répétiteur n'est pas disponible à cet horaire."
                )
                #Renvoye un message d'erreur s'il n'y a pas de disponibilité

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
    variable_envoi_recu = 'envoyée'

    return render (request, 'app/mes_demandes.html', {'demandes_liste' : demandes_liste, 'variable_envoi_recu': variable_envoi_recu})

@login_required
def mes_demandes_recues (request) : 
    demandes_liste = request.user.demandes_comme_prof.all()
    variable_envoi_recu = 'reçue'

    return render (request, 'app/mes_demandes.html', {'demandes_liste' : demandes_liste, 'variable_envoi_recu': variable_envoi_recu})

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