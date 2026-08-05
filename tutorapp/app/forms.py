from django import forms
from authentication.models import Sujet, User , NiveauEtudes

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
        label="Niveau(x) d'études"
    )

    tarif_max = forms.IntegerField(
        required=False,
        min_value=0,
        label="Tarif maximum"
        )