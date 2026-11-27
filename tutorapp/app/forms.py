from django import forms
from authentication.models import Sujet, User, NiveauEtudes, Disponibilite
from app.models import DemandeLecon

class ModifierCompteForm(forms.ModelForm):
   """Formulaire de modification des infos de base du compte"""
   # ModelForm, Django construit le formulaire automatiquement à partir du modèle,
   # et sait l'enregistrer (form.save()) sans qu'on écrive les champs à la main

   class Meta:
     model = User # le modèle sur lequel le formulaire est basé
     # Seuls ces champs apparaissent dans le formulaire (les autres ne sont pas modifiables ici)
     fields = (
        "email",
        "first_name",
        "last_name",
        "age",
        "ville",
        "bibliographie",
        "est_prof"
        )

class RechercheForm (forms.Form):
    """Formulaire de recherche de répétiteurs (les filtres)"""
    # Form (et pas ModelForm), ce formulaire n'enregistre rien dans la base de données,
    # Il sert seulement à récupérer les critères de recherche de l'élève
    # 'required=False' partout : on peut chercher avec un seul filtre, ou aucun

    last_name = forms.CharField(
        required=False,
        label="Nom"
        )

    # Liste déroulante remplie avec toutes les matières de la base de données
    matiere = forms.ModelChoiceField(
        queryset= Sujet.objects.all(),
        required=False,
        label="Matière"
        )

    ville = forms.CharField(
        required=False,
        label="Ville"
        )

    # Liste déroulante des niveaux d'études
    niveau_etudes = forms.ModelChoiceField(
        queryset= NiveauEtudes.objects.all(),
        required=False,
        label="Niveau d'études"
        )

    # Nombre entier qui refuse les valeurs négatives
    _max = forms.IntegerField(
        required=False,
        min_value=0,
        label="Tarif maximum"
        )

    # Choix du jour : on ajoute une option vide '------' devant la liste des jours
    # (réutilisée depuis le modèle Disponibilite pour ne pas la réécrire)
    jour = forms.ChoiceField(
        choices=[('','------')] + Disponibilite.JOURS,
        required=False,
        label="Jour",
        initial='',
        )

    # Heure précise recherchée (ex. : 14:30), comparée aux créneaux de disponibilité
    heure = forms.TimeField(
        required=False,
        label="Heure"
        )

class DemandeLeconForm (forms.ModelForm):
    """Formulaire de demande de leçon envoyé par l'élève."""

    # Champ ajouté « à la main » : il n'existe pas dans le modèle DemandeLecon
    # Il sert seulement à la vue pour savoir combien de demandes créer (1 = ponctuelle, plus = répétée chaque semaine)
    nombre_semaines = forms.IntegerField(
        initial=1,
        min_value=1,
        label="Nombre de semaines de répétition"
        )

    class Meta :
        model = DemandeLecon
        # eleve, prof et statut ne sont pas dans la liste : la vue les remplit elle-même 
        # (l'élève ne doit pas pouvoir les choisir ou les falsifier)
        fields = (
            'matiere',
            'date',
            'heure_debut',
            'heure_fin',
            'lieu',
        )

class StatutDemandeForm(forms.ModelForm):
    """Formulaire utilisé par le répétiteur pour accepter ou refuser une demande"""
    class Meta:
        model = DemandeLecon
        fields = ('statut',) # seul le statut est modifiable, le reste de la demande est protégé