import { fetchWithAuth } from "./auth.js";
import { logout } from "./auth.js";

const userZone = document.getElementById("user-zone");

async function renderUserHeader() {
    try {
        console.log("Tentative récupération profil...");
        console.log("Cookies envoyés :", document.cookie);

        const res = await fetchWithAuth("/api/profil/");
        console.log("Réponse profil:", res.status);

        if (!res.ok) {
            throw new Error("Non connecté");
        }

        const data = await res.json();
        console.log("Utilisateur reçu :", data);

        const isAdmin = data.role === "administrateur" || data.is_superuser;
        console.log("Cookies envoyés:", document.cookie);
        console.log("Réponse /api/profil :", res.status);
        userZone.innerHTML = `
            <div class="d-flex align-items-center gap-2">
                <button class="btn blue-bg-color btn-hover-b text-light rounded-1" id="profil-btn">👤 ${data.username}</button>
                <a href="/profil/" class="btn btn-outline-secondary">Profil</a>
                ${isAdmin ? `<a href="/admin/" class="btn btn-outline-secondary">Admin</a>` : ""}
                <button id="logout-btn" class="btn btn-danger">Déconnexion</button>
            </div>
        `;

        document.getElementById("logout-btn").addEventListener("click", logout);

    } catch (err) {
        console.warn("Erreur lors de la détection utilisateur :", err);
        userZone.innerHTML = `
            <a href="/connexion/" class="btn btn-primary me-2">Se connecter</a>
            <a href="/inscription/" class="btn btn-secondary">S'inscrire</a>
        `;
    }
}

document.addEventListener("DOMContentLoaded", renderUserHeader);
