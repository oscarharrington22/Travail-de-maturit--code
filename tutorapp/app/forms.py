from django import forms
from authentication.models import Sujet, User, NiveauEtudes, Disponibilite
from app.models import DemandeLecon

class ModifierCompteForm(forms.ModelForm):
   class Meta:
     model = User
     fields = (
        "first_name",
        "last_name",
        "ville",
        "bibliographie",
        "est_prof",
        "tarif",
        "niveau_etudes",
        "sujets_prof",)

class RechercheForm (forms.Form):
    matiere = forms.ModelChoiceField(
        queryset= Sujet.objects.all(),
        required=False,
        label="Matière"
        )

    ville = forms.CharField(
        required=False,
        label="Ville"
        )

    niveau_etudes = forms.ModelChoiceField(
        queryset= NiveauEtudes.objects.all(),
        required=False,
        label="Niveau d'études"
        )

    tarif_max = forms.IntegerField(
        required=False,
        min_value=0,
        label="Tarif maximum"
        )

    jour = forms.ChoiceField(
        choices=Disponibilite.JOURS,
        required=False,
        label="Jour"
        )

    heure = forms.TimeField(
        required=False,
        label="Heure"
        )

class DemandeLeconForm (forms.ModelForm):
    class Meta :
        model = DemandeLecon
        fields = (
            'matiere',
            'date',
            'heure',
            'lieu',)

class StatutDemandeForm(forms.ModelForm):
    class Meta:
        model = DemandeLecon
        fields = ('statut',)