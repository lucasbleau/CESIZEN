export async function fetchWithAuth(url, options = {}) {
    const access = localStorage.getItem("access");

    const csrfToken = getCSRFToken();

    options.headers = {
        "Content-Type": "application/json",
        Authorization: "Bearer " + access,
        "X-CSRFToken": csrfToken,
        ...options.headers, 
    };

    let response = await fetch(url, options);

    if (response.status === 401) {
        const refresh = localStorage.getItem("refresh");

        const refreshRes = await fetch("/api/token/refresh/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh }),
        });

        if (refreshRes.ok) {
            const data = await refreshRes.json();
            localStorage.setItem("access", data.access);
            options.headers.Authorization = "Bearer " + data.access;
            response = await fetch(url, options);
        } else {
            localStorage.clear();
            window.location.href = "/connexion/";
            return;
        }
    }

    return response;
}

function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        if (cookie.startsWith(name + "=")) {
            return cookie.split("=")[1];
        }
    }
    return "";
}

export function logout() {
    localStorage.clear();
    window.location.href = "/connexion/";
}

export function startAutoLogout(accessToken) {
    try {
        const payload = JSON.parse(atob(accessToken.split('.')[1]));
        const expTime = payload.exp * 1000;
        const now = Date.now();
        const delay = expTime - now;

        if (delay > 0) {
            setTimeout(() => {
                alert("Votre session a expiré. Vous avez été déconnecté.");
                logout();
            }, delay);
        }
    } catch (error) {
        console.error("Erreur de décodage du token :", error);
        logout();
    }
}

const existingAccessToken = localStorage.getItem("access");
if (existingAccessToken) {
    startAutoLogout(existingAccessToken);
}
