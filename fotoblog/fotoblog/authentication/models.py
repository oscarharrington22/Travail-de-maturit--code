from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class User (AbstractUser):
    TUTOR = 'Tuteur'
    STUDENT = 'Elève'

    ROLE_CHOICES = (
    (TUTOR, 'Tuteur'),
    (STUDENT, 'Elève'),
    )
    
    profile_photo = models.ImageField(verbose_name='Photo de profil')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')
    age = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(100)])
    ville = models.CharField()
    tariff = models.PositiveIntegerField(default=25, validators=[MinValueValidator(1)])