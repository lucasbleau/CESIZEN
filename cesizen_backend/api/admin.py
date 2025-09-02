print(">>> api.admin loaded")  # TEMP pour debug

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Utilisateur, ExerciceRespiration, HistoriqueExercice, Information

@admin.register(Utilisateur)
class UtilisateurAdmin(DjangoUserAdmin):
    ordering = ("-date_inscription",)
    list_display = ("email", "username", "role", "statut", "is_staff", "is_active", "last_login", "date_inscription")
    list_filter = ("role", "statut", "is_staff", "is_active", "date_inscription")
    search_fields = ("email", "username", "first_name", "last_name")
    readonly_fields = ("date_inscription", "last_login", "date_joined")
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Identité", {"fields": ("first_name", "last_name")}),
        ("Profil", {"fields": ("role", "statut")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_inscription", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "first_name", "last_name", "password1", "password2", "role", "statut", "is_staff", "is_active"),
        }),
    )

@admin.register(ExerciceRespiration)
class ExerciceRespirationAdmin(admin.ModelAdmin):
    list_display = ("nom", "duree_inspiration", "duree_apnee", "duree_expiration")
    search_fields = ("nom",)

@admin.register(HistoriqueExercice)
class HistoriqueExerciceAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "exercice", "date_effectue", "duree_totale")
    list_filter = ("date_effectue", "exercice")
    search_fields = ("utilisateur__email", "utilisateur__username", "exercice__nom")
    date_hierarchy = "date_effectue"

@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ("titre", "date_creation", "date_modification")
    search_fields = ("titre",)
    list_filter = ("date_creation", "date_modification")
print(">>> admin avancé chargé")