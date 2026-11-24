from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import User, Disponibilite

from authentication.forms import SignupProfForm
from .forms import RechercheForm, ModifierCompteForm, DemandeLeconForm, StatutDemandeForm
from app.models import DemandeLecon

from datetime import timedelta

def home(request):
    """Page d'accueil (accessible sans être connecté)"""
    return render(request, 'app/home.html')

@login_required
def mon_compte(request):
    """Affiche les informations du compte de l'utilisateur connecté"""
    return render(
        request,
        'app/mon_compte.html',
        {"user" : request.user}
        )

@login_required
def page_modification(request):
    """Page intermédiaire avec les liens vers les différentes modifications"""
    return render(request, 'app/page_modification.html')

@login_required
def modifier_compte(request):
    """Modifie les infos de base du compte (et envoie vers le profil répétiteur si besoin)"""
    user = request.user

    if request.method == "POST":
        form = ModifierCompteForm(request.POST, instance=user)
        # instance=user rempli le formulaire avec les donnée de l'instance user 
        # Permet de modifier les données déjà existantes

        if form.is_valid():
            form.save()
            if user.est_prof:
                # Un répétiteur passe ensuite au 2e formulaire (tarif, sujets, niveau)
                return redirect('modifier_compte_prof')
            return redirect('mon_compte')

    else:
        form = ModifierCompteForm(instance=user) # formulaire pré-rempli

    return render(
        request,
        'app/modifier_compte.html',
        {'form': form}
    )

@login_required
def modifier_compte_prof(request):
    """Modifie le profil de répétiteur (réutilise le formulaire de l'inscription)"""
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

def recherche (request):
    form = RechercheForm(request.GET)

    repetiteurs_liste = User.objects.filter(est_prof=True)
    # Prend tous les utilisateurs listés comme répétiteurs
    # Cette liste va être filtrée puis envoyée au gabarit pour être affichée

    if form.is_valid():
        last_name = form.cleaned_data["last_name"]
        ville = form.cleaned_data["ville"]
        matiere = form.cleaned_data["matiere"]
        tarif_max = form.cleaned_data["tarif_max"]
        niveau_etudes = form.cleaned_data["niveau_etudes"]
        jour = form.cleaned_data['jour']
        heure = form.cleaned_data['heure']
        # 'cleaned_data' récupère la valeur du champ indiqué pour pouvoir l'utiliser dans les filtres plus bas

        if request.user.is_authenticated and request.user.est_prof:
            repetiteurs_liste = repetiteurs_liste.exclude(id=request.user.id)
            # 'exclude' retire l'utilisateur de la liste (un répétiteur ne se trouve pas lui-même)

        # Chaque filtre n'est appliqué que si le champ a été rempli
        # Les filtres s'ajoutent les uns aux autres (ET logique)
        if last_name:
            repetiteurs_liste = repetiteurs_liste.filter(last_name=last_name)

        if ville:
            repetiteurs_liste = repetiteurs_liste.filter(ville=ville)

        if matiere:
            repetiteurs_liste = repetiteurs_liste.filter(sujets_prof=matiere)

        if tarif_max:
            repetiteurs_liste = repetiteurs_liste.filter(tarif__lte=tarif_max)
            # Ici, le '__' sert à clarifier que lte n'est pas un nom de champ et que c'est une focntion

        if niveau_etudes:
            repetiteurs_liste = repetiteurs_liste.filter(niveau_etudes=niveau_etudes)

        if jour:
            repetiteurs_liste = repetiteurs_liste.filter(disponibilites__jour=jour)
            # les 2 '__' indiquent qu'il faut aller chercher le champ jour dans le modèle Disponibilite
        if heure:
            repetiteurs_liste = repetiteurs_liste.filter(disponibilites__heure_debut__lte=heure, disponibilites__heure_fin__gte=heure)
            # lte signifie less than or equal (<=) et gte greater than or equal (>=)
            # Donc le créneau commence avant ou bien à l'heure cherchée et finit après

    return render(
        request,
        'app/recherche.html',
        {'form': form, 'repetiteurs_liste': repetiteurs_liste}
        )

def profil (request, user_id):
    """Page de profil public d'un répétiteur, avec ses disponibilités"""
    repetiteur = User.objects.get(id=user_id) # user_id vient de l'URL

    # Liste dans l'ordre de la semaine
    ordre_jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    # Objet django qui prend toutes des disponibilités
    queryset = Disponibilite.objects.filter(prof=repetiteur)

    # Dans la liste de disponibilités, sorted parcourt le queryset 1 par 1 et le trie selon la clé donnée
    # 'key' indique à 'sorted' selon quel critère trier, ici selon ce qui est renvoyé par la fonction lambda
    # 'lambda' est une fonction définie sur une ligne:
    # elle prend 'creneau' comme argument et renvoie le numero de jour et l'heure de chaque creneau dans queryset
    disponibilite_liste = sorted(queryset, key=lambda creneau: (ordre_jours.index(creneau.jour), creneau.heure_debut))

    return render(request, "app/profil.html",
        {
        "repetiteur": repetiteur,
         "disponibilite_liste": disponibilite_liste
         }
    )

@login_required
def demande_lecon (request, user_id):
    """Un élève envoie une demande de leçon (ponctuelle ou répétée) à un répétiteur"""
    prof = User.objects.get(id=user_id) # le répétiteur visé, d'après l'URL

    if request.method == 'POST':
        form = DemandeLeconForm(request.POST)

        if form.is_valid ():
            # 'commit=False', demande pas enregistrée pour y ajouter l'élève et le répétiteur (absents du formulaire)
            demande = form.save(commit=False)
            demande.eleve = request.user
            demande.prof = prof

            nombre_semaines = form.cleaned_data['nombre_semaines']
            # variable propre au formulaire (pas dans le modèle) : 1 = demande ponctuelle,
            # plus = demande répétée chaque semaine, sert à créer le bon nombre de demandes

            jours = [
                "lundi",
                "mardi",
                "mercredi",
                "jeudi",
                "vendredi",
                "samedi",
                "dimanche"
            ]
            # Liste de jours pour pouvoir utiliser l'index renvoyé par .weekday()
            # (weekday() donne 0 pour lundi, 1 pour mardi, etc.

            jour = jours[demande.date.weekday()] # nom du jour de la semaine correspondant à la date choisie

            disponibilite = Disponibilite.objects.filter(
                prof=prof,
                jour=jour,
                heure_debut__lte=demande.heure_debut,
                heure_fin__gte=demande.heure_fin
                ).exists()
               # 'exists', vérifie s'il existe un créneau de disponibilité ce pour ce prof ce jour-la
               # Doit couvrir entièrement l'horaire demandé (lte, gte)(Renvoie True ou False)

            if disponibilite:
                # Une demande est créée par semaine : même horaire, date décalée de 7 jours à chaque tour
                for semaine in range(nombre_semaines):
                    DemandeLecon.objects.create(
                        eleve=request.user,
                        prof=prof,
                        matiere=demande.matiere,
                        date=demande.date + timedelta(weeks=semaine),
                        # 'timedelta' sert à ajouter ou enlever un certain temps a une date (ici des semaines : 'week=')
                        heure_debut=demande.heure_debut,
                        heure_fin=demande.heure_fin,
                        lieu=demande.lieu
                    )
                return redirect("mes_demandes_envoyees")

            else:
                form.add_error(
                    None,
                    "Le répétiteur n'est pas disponible à cet horaire."
                )
                # None = erreur générale du formulaire (pas liée à un champ précis)
                # Renvoie un message d'erreur s'il n'y a pas de disponibilité

    else :
        form = DemandeLeconForm()

        form.fields['matiere'].queryset = prof.sujets_prof.all()
        # Les matières proposées dans le formulaire seront seulement celles que le prof enseigne
        # 'queryset' indique la liste d'objets (récupérée dans la base de données) parmi lesquels on peut choisir

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
    """Liste des demandes que l'utilisateur (élève) a envoyées"""
    demandes_liste = request.user.demandes_comme_eleve.all() # related_name défini dans le modèle
    variable_envoi_recu = 'envoyée' # sert au gabarit pour adapter les textes (même page que pour les reçues)

    return render (request, 'app/mes_demandes.html', {'demandes_liste' : demandes_liste, 'variable_envoi_recu': variable_envoi_recu})

@login_required
def mes_demandes_recues (request) : 
    """Liste des demandes que l'utilisateur (répétiteur) a reçues"""
    demandes_liste = request.user.demandes_comme_prof.all()
    variable_envoi_recu = 'reçue'

    return render (request, 'app/mes_demandes.html', {'demandes_liste' : demandes_liste, 'variable_envoi_recu': variable_envoi_recu})

@login_required
def repondre_demande(request, demande_id):
    """Le répétiteur accepte ou refuse une demande reçue (change son statut)"""
    demande = DemandeLecon.objects.get(id=demande_id)

    # Sécurité : seul le répétiteur concerné peut répondre à cette demande
    if demande.prof != request.user:
        return redirect("mes_demandes_recues")

    if request.method == 'POST':
        form = StatutDemandeForm(request.POST, instance=demande) # on modifie la demande existante

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
    """Supprime une demande, si l'utilisateur en est l'élève ou le répétiteur."""
    demande = DemandeLecon.objects.get(id=demande_id)

    # Sécurité : ni l'élève ni le répétiteur de la demande -> on redirige
    if demande.eleve != request.user and demande.prof != request.user:
        return redirect("mes_demandes_envoyees")

    demande.delete()

    return redirect("mes_demandes_envoyees")