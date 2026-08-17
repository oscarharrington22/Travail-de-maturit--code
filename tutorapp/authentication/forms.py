from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from authentication.models import Disponibilite

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = (
            'username',
            'email', 
            'first_name', 
            'last_name', 
            'age',
            'ville', 
            'est_prof', 
            'sujets_prof', 
            'niveau_etudes',
            'tarif' 
            )

class DisponibiliteForm(forms.ModelForm):
    class Meta :
        model = Disponibilite
        fields = (
            'jour',
            'heure_debut',
            'heure_fin',
            )

class UploadProfilePhotoForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('photo_de_profil', )