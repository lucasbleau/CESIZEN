import { fetchWithAuth, logout } from "./auth.js";

const userZone = document.getElementById("user-zone");

async function renderUserHeader() {
    const access = localStorage.getItem("access");

    if (!access) {
        userZone.innerHTML = `
            <a href="/connexion/" class="btn blue-bg-color btn-hover-b rounded-1 text-light me-4">Se connecter</a>
            <a href="/inscription/" class="btn blue-bg-color btn-hover btn-hover-b rounded-1 text-light">S'inscrire</a>
        `;
        return;
    }

    try {
        const res = await fetchWithAuth("/api/profil/");
        if (!res.ok) throw new Error();

        const data = await res.json();
        const isAdmin = data.role === "administrateur" || data.is_superuser;

        userZone.innerHTML = `
            <div class="d-flex align-items-center gap-2">
                <button class="btn blue-bg-color btn-hover-b text-light rounded-1" id="profil-btn">👤 ${data.username}</button>
                <a href="/profil/" class="btn btn-outline-secondary">Profil</a>
                <a href="/preferences/" class="btn btn-outline-secondary">Préférences</a>
                ${isAdmin ? `<a href="/admin/" class="btn btn-outline-secondary">Back office</a>` : ""}
                <button id="logout-btn" class="btn btn-danger btn-hover-r text-light">Déconnexion</button>
            </div>
        `;

        document.getElementById("logout-btn").addEventListener("click", logout);
    } catch (err) {
        console.warn("Erreur auth, redirection login...");
        localStorage.clear();
        window.location.href = "/connexion/";
    }
}

document.addEventListener("DOMContentLoaded", renderUserHeader);
