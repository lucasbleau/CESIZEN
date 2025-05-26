from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.admin.models import LogEntry

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('utilisateur', 'Utilisateur'),
        ('administrateur', 'Administrateur'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='utilisateur')
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='actif')

    def save(self, *args, **kwargs):
        if self.pk is None and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        HistoriqueExercice.objects.filter(utilisateur=self).delete()
        Information.objects.filter(createur=self).delete()
        LogEntry.objects.filter(user=self).delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

class ExerciceRespiration(models.Model):
    nom = models.CharField(max_length=100)
    duree_inspiration = models.IntegerField(help_text="Durée en secondes")
    duree_apnee = models.IntegerField(help_text="Durée en secondes")
    duree_expiration = models.IntegerField(help_text="Durée en secondes")
    description = models.TextField()

    def __str__(self):
        return self.nom

class HistoriqueExercice(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='historique_exercices')
    exercice = models.ForeignKey(ExerciceRespiration, on_delete=models.CASCADE, related_name='historique_exercices')
    date_effectue = models.DateTimeField(auto_now_add=True)
    duree_totale = models.IntegerField(help_text="Durée totale en secondes")
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.exercice.nom} - {self.date_effectue}"

class Information(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    createur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='informations_crees')

    def __str__(self):
        return self.titre
