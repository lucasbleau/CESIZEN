from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.models import Utilisateur

def accueil(request):
    return render(request, 'accueil.html')  


def liste_utilisateurs(request):
    # Récupérez tous les utilisateurs
    utilisateurs = Utilisateur.objects.all()
    # Passez les utilisateurs au template
    return render(request, 'liste_utilisateurs.html', {'utilisateurs': utilisateurs})


def connexion(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):
            login(request, user)
            messages.success(request, 'Connexion réussie ! Bienvenue.')
            return redirect('accueil')
        else:
            messages.error(request, 'Email ou mot de passe incorrect')

    return render(request, 'connexion.html')


@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect("connexion")
