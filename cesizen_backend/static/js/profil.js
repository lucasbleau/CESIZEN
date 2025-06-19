import { fetchWithAuth } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    const table = document.getElementById("profil-table");
    const lastLoginText = document.getElementById("last-login-text");
    const historiqueTable = document.getElementById("historique-table");

    const res = await fetchWithAuth("/api/profil/");
    const data = await res.json();

    if (res.ok) {
        const fields = {
            "Nom d'utilisateur": data.username || "<i>Non spécifié</i>",
            "Email": data.email || "<i>Non spécifié</i>",
            "Prénom": data.first_name || "<i>Non spécifié</i>",
            "Nom": data.last_name || "<i>Non spécifié</i>"
        };

        table.innerHTML = "";
        for (const [label, value] of Object.entries(fields)) {
            const row = `
                <tr>
                    <td class="fw-bold text-center align-middle">${label}</td>
                    <td class="text-center">${value}</td>
                </tr>`;
            table.innerHTML += row;
        }

        const lastLoginElement = document.getElementById("last-login-info");
        lastLoginElement.textContent = data.last_login
            ? `Dernière connexion : ${new Date(data.last_login).toLocaleString()}`
            : "Dernière connexion : inconnue";

    } else {
        table.innerHTML = `<tr><td colspan="2" class="text-danger text-center">Erreur chargement profil.</td></tr>`;
    }

    const histoRes = await fetchWithAuth("/api/historique/");
    if (histoRes.ok) {
        const historique = await histoRes.json();
        historiqueTable.innerHTML = "";

        if (historique.length === 0) {
            historiqueTable.innerHTML = `<tr><td colspan="3" class="text-center text-muted">Aucun exercice réalisé.</td></tr>`;
        } else {
            historique.forEach(item => {
                const row = `
                    <tr>
                        <td>${item.nom_exercice}</td>
                        <td>${new Date(item.date).toLocaleString()}</td>
                        <td>${item.duree}</td>
                    </tr>
                `;
                historiqueTable.innerHTML += row;
            });
        }
    } else {
        historiqueTable.innerHTML = `<tr><td colspan="3" class="text-danger text-center">Erreur chargement historique.</td></tr>`;
    }
});
