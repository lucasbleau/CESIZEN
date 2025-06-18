export async function fetchWithAuth(url, options = {}, retry = true) {
    options.credentials = "include";

    if (!options.headers) options.headers = {};
    options.headers["Content-Type"] = "application/json";

    let response = await fetch(url, options);

    if (response.status === 401 && retry) {
        const publicPaths = ["/connexion/", "/inscription/", "/", "/exercices/"];
        if (publicPaths.includes(window.location.pathname)) {
            return response; 
        }

        console.warn("Token expiré, tentative de rafraîchissement...");
        const refresh = await fetch("/api/token/refresh-cookie/", {
            method: "POST",
            credentials: "include",
        });

        if (refresh.ok) {
            return await fetchWithAuth(url, options, false);
        } else {
            console.warn("Échec du refresh. Redirection connexion...");
            window.location.href = "/connexion/";
        }
    }

    return response;
}

export function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        if (cookie.startsWith(name + "=")) {
            return cookie.split("=")[1];
        }
    }
    return "";
}


export async function logout() {
    try {
        await fetch("/api/deconnexion/", {
            method: "POST",
            credentials: "include",
        });
    } catch (err) {
        console.warn("Erreur pendant la déconnexion :", err);
    }

    window.location.href = "/connexion/";
}
