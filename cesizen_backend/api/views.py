from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from api.models import Utilisateur

def accueil(request):
    user_id = request.session.get('_auth_user_id')  # Récupère l'ID utilisateur en session
    print(f"Session User ID : {user_id}")  # Debugging

    if request.user.is_authenticated:
        print(f"Utilisateur authentifié : {request.user}")
    else:
        print("Aucun utilisateur connecté !")

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

        user = authenticate(request, username=email, password=password)  # Vérifie les credentials

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

        # Vérifications
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, "inscription.html")

        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
            return render(request, "inscription.html")

        if Utilisateur.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, "inscription.html")

        # Création de l'utilisateur
        utilisateur = Utilisateur.objects.create_user(
            email=email,
            username=username,
            password=password1
        )

        # 🔹 Récupérer l'utilisateur via `authenticate` pour identifier le bon backend
        user = authenticate(request, email=email, password=password1)

        if user:
            login(request, user)  # 🔹 Connexion automatique
            messages.success(request, "Inscription réussie !")
            return redirect("accueil")  # Redirige vers la page d'accueil ou de profil

    return render(request, "inscription.html")



@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect("accueil")
