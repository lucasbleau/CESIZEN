from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.admin.models import LogEntry

# Modèle Utilisateur personnalisé
class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('utilisateur', 'Utilisateur'),
        ('administrateur', 'Administrateur'),
    ]

    email = models.EmailField(unique=True)  # Assure-toi que l'email est unique
    username = models.CharField(max_length=150, unique=True)
    USERNAME_FIELD = 'email'  # Authentification via email
    REQUIRED_FIELDS = ['username']  # Le champ 'username' est nécessaire lors de la création via createsuperuser
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='utilisateur')
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='actif')

    # Ajoutez ces lignes pour résoudre le conflit de related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="utilisateur_groups",  # Nom personnalisé pour éviter le conflit
        related_query_name="utilisateur",
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="utilisateur_permissions",  # Nom personnalisé pour éviter le conflit
        related_query_name="utilisateur",
    )

    def save(self, *args, **kwargs):
        if self.pk is None and not self.password.startswith('pbkdf2_'):
            self.set_password(self.password)  # Hash le mot de passe seulement à la création
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        HistoriqueExercice.objects.filter(utilisateur=self).delete()
        Information.objects.filter(createur=self).delete()
        LogEntry.objects.filter(user=self).delete()  # C'est crucial pour les logs d'admin !
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
    

# Modèle Exercice de Respiration
class ExerciceRespiration(models.Model):
    nom = models.CharField(max_length=100)
    duree_inspiration = models.IntegerField(help_text="Durée en secondes")
    duree_apnee = models.IntegerField(help_text="Durée en secondes")
    duree_expiration = models.IntegerField(help_text="Durée en secondes")
    description = models.TextField()

    def __str__(self):
        return self.nom

# Modèle Historique des Exercices
class HistoriqueExercice(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='historique_exercices')
    exercice = models.ForeignKey(ExerciceRespiration, on_delete=models.CASCADE, related_name='historique_exercices')
    date_effectue = models.DateTimeField(auto_now_add=True)
    duree_totale = models.IntegerField(help_text="Durée totale en secondes")
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.exercice.nom} - {self.date_effectue}"

# Modèle Information
class Information(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    createur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='informations_crees')

    def __str__(self):
        return self.titre