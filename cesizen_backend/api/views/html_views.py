import json
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.models import Utilisateur, ExerciceRespiration, HistoriqueExercice, Information
from django.core.serializers.json import DjangoJSONEncoder

def accueil(request):
    informations = Information.objects.all()
    return render(request, 'accueil.html', {'informations': informations})


def profil(request):
    return render(request, "profil.html")

@login_required
def profil_edit(request):
    user = request.user

    if request.method == "POST":
        user.username = request.POST.get("Nom d'utilisateur", user.username)
        user.email = request.POST.get("Email", user.email)
        user.first_name = request.POST.get("Prénom", user.first_name)
        user.last_name = request.POST.get("Nom", user.last_name)

        user.save()
        return redirect('profil')

    user_info = {
        "Nom d'utilisateur": user.username,
        "Email": user.email,
        "Prénom": user.first_name,
        "Nom": user.last_name,
    }

    return render(request, 'profil_edit.html', {'user_info': user_info})



def preferences(request):
    return render(request, 'preferences.html')

@login_required
def upgrade_to_admin(request, user_id):
    user = get_object_or_404(Utilisateur, id=user_id)
    user.role = "administrateur"
    user.save()
    return redirect('profil')


def connexion(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('accueil')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")

    return render(request, 'connexion.html')



def inscription(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "inscription.html")

        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, "inscription.html")

        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, "inscription.html")

        utilisateur = Utilisateur.objects.create_user(
            email=email,
            username=username,
            password=password1
        )

        user = authenticate(request, email=email, password=password1)

        if user:
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect("accueil")

    return render(request, "inscription.html")


@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect("accueil")

def exercices(request):
    return render(request, "exercices.html")

def exercice_run(request, id):
    exercice = get_object_or_404(ExerciceRespiration, id=id)
    exercice_json = json.dumps({
        "id": exercice.id,
        "duree_inspiration": exercice.duree_inspiration,
        "duree_apnee": exercice.duree_apnee,
        "duree_expiration": exercice.duree_expiration,
    }, cls=DjangoJSONEncoder)
    return render(request, "exercice_run.html", {
        "exercice": exercice,
        "exercice_json": exercice_json
    })
