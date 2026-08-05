from django import forms
from authentication.models import Sujet, User 

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

    tarif_max = forms.IntegerField(
        required=False,
        min_value=0,
        label="Tarif maximum"
        )