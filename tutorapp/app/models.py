from django.db import models
from authentication.models import Sujet, User

class DemandeLecon (models.Model):
    """Une demande de leçon envoyée par un élève à un répétiteur."""

    # Les 3 états possibles d'une demande : (valeur stockée, texte affiché)
    STATUT_CHOIX = [
        ("en_attente", "En attente"),
        ("acceptee", "Acceptée"),
        ("refusee", "Refusée"),
    ]

    # Élève qui fait la demande, les élèves et les répétiteurs sont tous des User (deux ForeignKey diff vers User)
    # 'related_name' est obligatoire pour distinguer les deux ForeignKey
    # 'on_delete=models.CASCADE', si l'élève est supprimé, ses demandes le sont aussi.
    eleve = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Élève',
        related_name="demandes_comme_eleve",
    )

     # Répétiteur qui reçoit la demande, fonctionne de la mm manière que l'élève
    prof = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Répetiteur',
        related_name="demandes_comme_prof",
    )

    # Matière de la leçon, choisie parmi les Sujet existants
    matiere = models.ForeignKey(
        Sujet,
        on_delete=models.CASCADE,
        verbose_name='Matière'
    )

    # Date, créneau horaire et lieu souhaités par l'élève
    date = models.DateField(verbose_name='Date')

    heure_debut = models.TimeField(verbose_name='Heure de début')

    heure_fin = models.TimeField(verbose_name='Heure de fin')
    
    lieu = models.CharField(verbose_name='Lieu', max_length=64)

    # État de la demande, en attente par défaut, puis le répétiteur la passe à acceptée ou refusée
    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOIX,
        default="en_attente",
        verbose_name="Statut"
    )