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
function logoutLink() {
  // Fallback: GET vers l’endpoint (redirige vers /)
  return `<a class="toggle-btn active" href="/api/token/cookie/logout/?next=/" data-logout>Déconnexion</a>`;
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
        ${logoutLink()}
      </div>`;
    const a = zone.querySelector("[data-logout]");
    a.addEventListener("click", async (e) => {
      // Intercepte l’ancre pour faire un POST propre
      e.preventDefault();
      e.stopPropagation();
      try {
        await fetch("/api/token/cookie/logout/", { method: "POST", credentials: "include" });
      } catch {}
      // Redirige ensuite vers la home
      window.location.href = "/";
    });
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
