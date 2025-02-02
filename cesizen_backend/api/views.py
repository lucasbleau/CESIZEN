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

        try:
            user = Utilisateur.objects.get(email=email)
        except Utilisateur.DoesNotExist:
            user = None

        if user is not None and user.check_password(password):  
            login(request, user)
            request.session.save()  # Force la sauvegarde de session
            # messages.success(request, "Connexion réussie !")
            messages.success(request, f"Session ID : {request.session.session_key}")
            return redirect('accueil')

    return render(request, 'connexion.html')

def inscription(request):
    return render(request, 'inscription.html')

@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, "Déconnexion réussie !")
    return redirect("accueil")
