from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import time

class Sujet(models.Model):
    """Une matière qu'un répétiteur peut enseigner """
    nom = models.CharField(max_length=100, verbose_name='Nom du sujet')

    def __str__(self):
        # Affiche le nom du sujet dans les listes déroulantes
        return self.nom

class NiveauEtudes(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Niveau d'études")

    def __str__(self):
        return self.nom

class User (AbstractUser):
    """
    Extension du modèle utilisateur de base de Django (qui gère déjà nom d'utilisateur,
    mot de passe et e-mail) avec des champs supplémentaires
    Un même modèle sert aux élèves et aux répétiteurs : c'est le booléen 'est_prof' qui les différencie
    """

    # Photo facultative (nécessite Pillow)
    photo_de_profil = models.ImageField(
        verbose_name='Photo de profil',
        null=True, 
        blank=True
        )

    # Âge compris entre 1 et 100 (18 par défaut)
    age = models.PositiveIntegerField(
        default=18, 
        validators=[MinValueValidator(1), MaxValueValidator(100)], 
        verbose_name='Âge'
        )

    # Ville utilisée plus tard comme filtre dans la recherche de répétiteurs    
    ville = models.CharField(
        max_length=20, 
        verbose_name="Lieu d'habitation"
        )

    # Courte présentation du répétiteur (facultatif)
    bibliographie = models.CharField(
        max_length=200, 
        verbose_name="Biographie",
        blank=True,
        null=True
    )

    # Case cochée à l'inscription (ou plus tard) pour devenir répétiteur
    est_prof = models.BooleanField(
        default=False, 
        verbose_name='Peut donner des cours'
        )

    # Matières enseignées : un répétiteur peut en avoir plusieurs et une
    # matière peut être enseignée par plusieurs répétiteurs (ManyToMany)
    sujets_prof = models.ManyToManyField(
        Sujet,
        blank=True,  
        verbose_name='Sujets enseignés'       
        )

    # Tarif à l'heure, uniquement pour les répétiteurs (null=True)
    tarif = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], 
        verbose_name="Tarif à l'heure" ,
        null=True
        )
    
    # Niveau d'études s'il est supprimé de la base : 
    # l'utilisateur est conservé et son niveau passe à NULL (on_delete = models.SET_NULL)
    niveau_etudes = models.ForeignKey(
        NiveauEtudes,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Niveau d'études"
    )

class Disponibilite(models.Model):
    """
    Un créneau de disponibilité d'un répétiteur
    Un répétiteur peut avoir plusieurs créneaux qui servent de filtre dans
    la recherche
    """

    # Valeurs possibles pour le jour (valeur stockée ; texte affiché)
    JOURS = [
        ("lundi", "Lundi"),
        ("mardi", "Mardi"),
        ("mercredi", "Mercredi"),
        ("jeudi", "Jeudi"),
        ("vendredi", "Vendredi"),
        ("samedi", "Samedi"),
        ("dimanche", "Dimanche"),
    ]

    # Répétiteur.CASCADE : si l'utilisateur est supprimé, ses disponibilités le sont aussi
    # related_name permet d'écrire `user.disponibilites.all()` pour recuperer les disponibilités de ce repetiteur
    # Relation ForeignKey (1 à plusieurs)
    # 1 repetiteurs peut-être lié a plusieures disponibilités mais une disponibilité n'a qu'un repetiteur
    prof = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="disponibilites"
    )

    jour = models.CharField(
        max_length=10,
        choices=JOURS,
    )

    # Début et fin du créneau
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
