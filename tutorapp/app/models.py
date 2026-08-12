from django.db import models
from authentication.models import Sujet, User

class DemandeLecon (models.Model):

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

    status = models.BooleanField(verbose_name='Status', default=False)