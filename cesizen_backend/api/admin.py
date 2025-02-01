from django.contrib import admin
from .models import Utilisateur, ExerciceRespiration, HistoriqueExercice, Information

# Personnalisation pour le modèle ExerciceRespiration
class ExerciceRespirationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'duree_inspiration', 'duree_apnee', 'duree_expiration')
    search_fields = ('nom',)
    list_filter = ('duree_inspiration', 'duree_expiration')

# Personnalisation pour le modèle Utilisateur
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'date_inscription')
    search_fields = ('username', 'email')
    list_filter = ('role', 'date_inscription')

# Personnalisation pour le modèle HistoriqueExercice
class HistoriqueExerciceAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'exercice', 'date_effectue', 'duree_totale')
    search_fields = ('utilisateur__username', 'exercice__nom')
    list_filter = ('date_effectue', 'exercice')

# Personnalisation pour le modèle Information
class InformationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'createur', 'date_creation', 'date_modification')
    search_fields = ('titre', 'createur__username')
    list_filter = ('date_creation', 'date_modification')

# Enregistrement des modèles avec leurs classes ModelAdmin
admin.site.register(Utilisateur, UtilisateurAdmin)
admin.site.register(ExerciceRespiration, ExerciceRespirationAdmin)
admin.site.register(HistoriqueExercice, HistoriqueExerciceAdmin)
admin.site.register(Information, InformationAdmin)