from django import forms
from . import Sujet, User 

class RechercheForm (forms.Form):
    matiere = forms.ModelChoiceField(
        queryset= Sujet.objects.all(),
        required=False,
        verbose_name="Matière"
        )

    ville = forms.CharField(
        required=False,
        verbose_name="Ville"
        )

    tarif_max = forms.IntegerField(
        required=False,
        min_value=0,
        verbose_name="Tarif maximum"
        )