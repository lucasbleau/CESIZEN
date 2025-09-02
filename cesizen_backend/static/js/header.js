import { fetchWithAuth, logout } from "./auth.js";

// Remplacement complet

// Helpers locaux (en cas d'absence de fetchWithAuth fiable)
async function fetchProfile() {
  return fetch("/api/profil/", { credentials: "include" });
}
async function tryRefreshIf401(res) {
  if (res.status !== 401) return res;
  const r = await fetch("/api/token/cookie/refresh/", {
    method: "POST",
    credentials: "include",
  });
  if (!r.ok) return res; 
  return fetchProfile();
}
function btn(html, extra="") {
  return `<button class="toggle-btn ${extra}">${html}</button>`;
}
async function renderUserHeader() {
  const zone = document.getElementById("user-zone");
  if (!zone) return;
  try {
    let r = await fetchProfile();
    r = await tryRefreshIf401(r);
    if (!r.ok) throw 0;
    const data = await r.json();
    zone.innerHTML = `
      <div class="d-flex align-items-center gap-2">
        <a href="/profil/" class="toggle-btn">${data.username || data.email}</a>
        ${data.is_superuser ? `<a href="/admin/" class="toggle-btn">Admin</a>` : ""}
        ${btn("Déconnexion","active")} 
      </div>`;
    zone.querySelector(".toggle-btn.active").onclick = async () => {
      await fetch("/api/token/cookie/logout/", { method:"POST", credentials:"include" });
      location.reload();
    };
  } catch {
    zone.innerHTML = `
      <a href="/connexion/" class="toggle-btn primary">Se connecter</a>
      <a href="/inscription/" class="toggle-btn outline">S'inscrire</a>
    `;
  }
}

// Re-render après DOM chargé ou après login custom
document.addEventListener("DOMContentLoaded", renderUserHeader);

// Expose pour réutilisation après un login AJAX sans reload
window.refreshUserHeader = renderUserHeader;
