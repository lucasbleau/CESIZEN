const PUBLIC_PATHS = ["/", "/connexion/", "/inscription/", "/exercices/"];

function isPublic(pathname = window.location.pathname) {
  return PUBLIC_PATHS.some(
    p => pathname === p || (p === "/exercices/" && pathname.startsWith("/exercices/"))
  );
}


export async function fetchWithAuth(url, options = {}, retry = true) {
  options.credentials = "include";
  options.headers = { "Content-Type": "application/json", ...(options.headers || {}) };

  let response = await fetch(url, options);

  if (response.status === 401 && retry && !isPublic()) {
    console.warn("Token expiré – tentative de rafraîchissement…");

    const refresh = await fetch("/api/token/refresh-cookie/", {
      method: "POST",
      credentials: "include",
    });

    if (refresh.ok) {
      return fetchWithAuth(url, options, false); 
    }

    console.warn("Refresh KO. Redirection vers /connexion/…");
    window.location.href = "/connexion/";
  }

  return response;
}


export function getCSRFToken() {
  const tokenCookie = document.cookie
    .split("; ")
    .find(c => c.startsWith("csrftoken="));

  return tokenCookie ? tokenCookie.split("=")[1] : "";
}


export async function logout() {
  try {
    await fetch("/api/deconnexion/", { method: "POST", credentials: "include" });
  } catch (err) {
    console.warn("Erreur pendant la déconnexion :", err);
  }
  window.location.href = "/connexion/";
}
