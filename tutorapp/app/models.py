from django.db import models
from authentication.models import Sujet, User

class DemandeLecon (models.Model):

    STATUT_CHOIX = [
        ("en_attente", "En attente"),
        ("acceptee", "Acceptée"),
        ("refusee", "Refusée"),
    ]

    eleve = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Élève',
        related_name="demandes_comme_eleve",
    )

    prof = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Répetiteur',
        related_name="demandes_comme_prof",
    )

    matiere = models.ForeignKey(
        Sujet,
        on_delete=models.CASCADE,
        verbose_name='Matière'
    )

    date = models.DateField(verbose_name='Date')

    heure = models.TimeField(verbose_name='Heure')
    
    lieu = models.CharField(verbose_name='Lieu', max_length=64)

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOIX,
        default="en_attente",
        verbose_name="Statut"
    )