from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class Sujet(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom du sujet')

    def __str__(self):
        return self.nom

class NiveauEtudes(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Niveau d'études")

    def __str__(self):
        return self.nom

class User (AbstractUser):

    photo_de_profil = models.ImageField(
        verbose_name='Photo de profil',
        null=True, 
        blank=True
        )
    age = models.PositiveIntegerField(
        default=10, 
        validators=[MinValueValidator(1), MaxValueValidator(100)], 
        verbose_name='Âge'
        )
    ville = models.CharField(
        max_length=20, 
        verbose_name="Lieu d'habitation"
        )

    bibliographie = models.CharField(
        max_length=200, 
        verbose_name="Bibliographie",
        blank=True,
        null=True
    )

    est_prof = models.BooleanField(
        default=False, 
        verbose_name='Peut donner des cours'
        )

    sujets_prof = models.ManyToManyField(
        Sujet,
        blank=True,  
        verbose_name='Sujets enseignés'       
        )

    tarif = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], 
        verbose_name="Tariff à l'heure" ,
        blank=True,
        null=True
        )
    
    niveau_etudes = models.ForeignKey(
        NiveauEtudes,
        on_delete=models.SET_NULL,
        blank =True,
        null=True,
        verbose_name="Niveau d'études"
    )