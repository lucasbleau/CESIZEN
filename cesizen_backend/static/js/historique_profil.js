import { fetchWithAuth } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    const tableBody = document.getElementById("historique-table");

    const res = await fetchWithAuth("/api/historique/");
    if (!res.ok) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="3" class="text-danger text-center">Erreur lors du chargement de l'historique.</td>
            </tr>`;
        return;
    }

    const data = await res.json();
    if (data.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="3" class="text-center text-muted">Aucun exercice effectué pour le moment.</td>
            </tr>`;
        return;
    }

    tableBody.innerHTML = "";

    data.forEach(entry => {
        const row = `
            <tr>
                <td>${entry.exercice_nom}</td>
                <td>${new Date(entry.date_effectue).toLocaleString()}</td>
                <td>${entry.duree_totale} s</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
});
