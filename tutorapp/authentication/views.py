from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Disponibilite
from . import forms

def logout_user(request):
    """Déconnecte l'utilisateur et le renvoie à la page de connexion"""
    logout(request)
    return redirect('login')

def signup_page(request):
    """Page d'inscription : crée le compte, connecte l'utilisateur, puis l'oriente"""
    form = forms.SignupForm() # formulaire vide (affichage de la page, requête GET)

    # POST = l'utilisateur a cliqué sur « S'inscrire »
    if request.method == 'POST':
        form = forms.SignupForm(request.POST) # on remplit le formulaire avec ses données

        # is_valid() vérifie la validité des champs
        if form.is_valid():
            user = form.save() # crée l'utilisateur dans la base de données
            login(request, user) # connecte directement l'utilisateur
            
            # Si 'Peut donner des cours' est coché il doit d'abord remplir son profil de répétiteur
            if user.est_prof:
                return redirect('signup_prof')

            return redirect(settings.LOGIN_REDIRECT_URL) # si pas prof, renvoie vers l'url d'après login défini dans settings

    return render(request, 'authentication/signup.html', context={'form': form})

@login_required # il faut être connecté pour accéder à cette page
def signup_prof(request):
    """Formulaire du profil de répétiteur (tarif, sujets, niveau d'études)"""
    form = forms.SignupProfForm(instance=request.user) # pré-rempli avec les infos de l'utilisateur ('instance=request.user')

    if request.method == 'POST':
        form = forms.SignupProfForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'authentication/signup_prof.html', context={'form': form})


@login_required
def upload_profile_photo(request):
    """Permet à l'utilisateur de changer sa photo de profil"""
    form = forms.UploadProfilePhotoForm(instance=request.user) # 'instance=request.user' on modifie l'utilisateur existant

    if request.method == 'POST':
        # 'request.FILES' est nécessaire pour recevoir le fichier image envoyé
        form = forms.UploadProfilePhotoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mon_compte')
    return render(request, 'authentication/upload_profile_photo.html', context={'form': form})

@login_required
def mes_disponibilites(request):
    """Affiche les créneaux de disponibilité du répétiteur connecté, triés par jour puis heure"""

    # Liste dans l'ordre de la semaine
    ordre_jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']
    # Objet djanog qui prend toutes des disponibilités
    queryset = request.user.disponibilites.all()

    # Dans la liste de disponibilités, sorted parcour le queryset 1 par 1 et le trie selon la clé donnée
    # 'key' indique à 'sorted' selon quel critère trier, ici selon ce qui est renvoyé par la fonction lambda
    # 'lambda' est une fonction definie sur une ligne:
    # elle prend 'creneau' comme argument et renvoie le numero de jour et l'heure de chaque creneau dans queryset
    disponibilites_liste = sorted(queryset, key=lambda creneau: (ordre_jours.index(creneau.jour), creneau.heure_debut))

    # Seuls les répétiteurs ont des disponibilités, les autres retournent à l'accueil
    if not request.user.est_prof:
        return redirect('home')

    return render(request, 'authentication/mes_disponibilites.html',{'disponibilites_liste': disponibilites_liste})

@login_required
def nouvelle_disponibilite(request):
    """Ajoute un nouveau créneau de disponibilité pour un répétiteur connecté"""
    if request.method == 'POST':
        form = forms.DisponibiliteForm(request.POST)
        if form.is_valid():
            # 'commit=False', on crée l'objet sans l'enregistrerpour pouvoir y ajouter le répétiteur (qui n'est pas dans le formulaire)
            creneau = form.save(commit=False)
            creneau.prof = request.user # on lie le créneau à l'utilisateur connecté
            creneau.save() # maintenant on enregistre
            return redirect('mes_disponibilites')
        
    else:
        form = forms.DisponibiliteForm() # formulaire vide à la première visite
    
    return render(request, 'authentication/nouvelle_disponibilite.html', {'form' : form})

@login_required
def supprimer_disponibilite(request, id):
    """Supprime un créneau, à condition qu'il appartienne à l'utilisateur connecté """
    # 'prof=request.user' empêche de supprimer le créneau d'un autre répétiteur en changeant l'id dans l'URL
    creneau = Disponibilite.objects.get(id=id, prof=request.user)
    creneau.delete()
    return redirect('mes_disponibilites')