import { fetchWithAuth } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("historique-container");

    const res = await fetchWithAuth("/api/historique/");
    console.log("Profil API status:", res.status);
    if (!res.ok) {
        container.innerHTML = "<p class='text-danger'>Erreur lors du chargement de l'historique.</p>";
        return;
    }

    const data = await res.json();
    if (data.length === 0) {
        container.innerHTML = "<p>Aucun exercice effectué pour le moment.</p>";
        return;
    }

    const table = document.createElement("table");
    table.className = "table table-striped";
    table.innerHTML = `
        <thead>
            <tr>
                <th>Exercice</th>
                <th>Date</th>
                <th>Durée (s)</th>
            </tr>
        </thead>
        <tbody>
            ${data.map(entry => `
                <tr>
                    <td>${entry.exercice_nom}</td>
                    <td>${new Date(entry.date_effectue).toLocaleString()}</td>
                    <td>${entry.duree_totale}</td>
                </tr>
            `).join('')}
        </tbody>
    `;

    container.innerHTML = "";
    container.appendChild(table);
});
