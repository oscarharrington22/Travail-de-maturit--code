from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class User (AbstractUser):

    profile_photo = models.ImageField(
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
        max_length=100, 
        verbose_name="Lieu d'habitation"
        )

    est_prof = models.BooleanField(
        default=False, 
        verbose_name='Peu donner des cours'
        )

    sujets_prof = models.ManyToManyField(Sujet, blank=True, verbose_name='Sujets enseignés')

    tarif = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], 
        verbose_name="Tariff à l'heure" ,
        blank=True,
        null=True
        )
    
class Sujet(models.Model):
    nom = models.CharField(max_length=100, verbose_name='Nom du sujet')

    def __str__(self):
        return self.nom