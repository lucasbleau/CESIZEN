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
        console.log("Utilisateur reçu :", data);
        userZone.innerHTML = `
            <div class="d-flex align-items-center gap-2">
                <a href="/profil/" class="toggle-btn">👤 ${data.username}</a>
                ${isAdmin ? `<a href="/admin/" class="toggle-btn">Admin</a>` : ""}
                <button id="logout-btn" class="toggle-btn active">Déconnexion</button>
            </div>
        `;

        document.getElementById("logout-btn").addEventListener("click", logout);

    } catch (err) {
        console.warn("Erreur lors de la détection utilisateur :", err);
        userZone.innerHTML = `
            <a href="/connexion/" class="toggle-btn active">Se connecter</a>
            <a href="/inscription/" class="toggle-btn">S'inscrire</a>
        `;
    }
}

document.addEventListener("DOMContentLoaded", renderUserHeader);
