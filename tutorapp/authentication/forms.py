from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User, Disponibilite

class SignupForm(UserCreationForm):
    """Formulaire d'inscription : crée un nouveau compte (élève ou répétiteur)."""
    # UserCreationForm est le formulaire d'inscription prêt à l'emploi de Django.
    # Il ajoute tout seul les champs « mot de passe » et « confirmation »

    class Meta(UserCreationForm.Meta):
        # On reprend le Meta de Django (Meta(UserCreationForm.Meta)) et on change ce qui nous concerne (le modèle et les champs)
        model = get_user_model() # renvoie notre modèle User personnalisé (celui de settings.py)
        fields = (
            'username',
            'email', 
            'first_name', 
            'last_name', 
            'age',
            'ville', 
            'est_prof', 
            )

class SignupProfForm(forms.ModelForm):
    """Formulaire du profil de répétiteur (2e étape de l'inscription, et modification du profil)"""
    # Les infos propres aux répétiteurs sont séparées de l'inscription de base
    # Pour ne les demander qu'à ceux qui ont coché est_prof
    class Meta :
        model = User
        fields = (
            'sujets_prof', # matières enseignées (relation ManyToMany)
            'niveau_etudes',
            'tarif',
            )

class DisponibiliteForm(forms.ModelForm):
    """Formulaire d'ajout d'un créneau de disponibilité"""
    class Meta :
        # 'prof' n'est pas dans la liste, la vue le remplit avec l'utilisateur connecté (commit=False)
        # Pour qu'on ne puisse pas ajouter un créneau au nom de quelqu'un d'autre
        model = Disponibilite
        fields = (
            'jour',
            'heure_debut',
            'heure_fin',
            )

class UploadProfilePhotoForm(forms.ModelForm):
    """Formulaire pour changer sa photo de profil."""
    class Meta:
        model = get_user_model()
        fields = ('photo_de_profil', )