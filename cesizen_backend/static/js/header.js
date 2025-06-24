import { fetchWithAuth, logout } from "./auth.js";

const userZone = document.getElementById("user-zone");

async function renderUserHeader() {
  try {
    const res = await fetchWithAuth("/api/profil/");
    if (!res.ok) throw new Error("401");

    const data    = await res.json();
    const isAdmin = data.role === "administrateur" || data.is_superuser;

    userZone.innerHTML = `
      <div class="d-flex align-items-center gap-2">
        <a href="/profil/" class="toggle-btn">👤 ${data.username}</a>
        ${isAdmin ? `<a href="/admin/" class="toggle-btn">Admin</a>` : ""}
        <button id="logout-btn" class="toggle-btn active">Déconnexion</button>
      </div>
    `;
    document.getElementById("logout-btn").addEventListener("click", logout);
  } catch (err) {
    userZone.innerHTML = `
      <a href="/connexion/" class="toggle-btn active">Se connecter</a>
      <a href="/inscription/" class="toggle-btn">S'inscrire</a>
    `;
  }
}

document.addEventListener("DOMContentLoaded", renderUserHeader);
