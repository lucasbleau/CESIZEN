import { fetchWithAuth } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    const res = await fetchWithAuth("/api/profil/");
    const data = await res.json();

    if (res.ok) {
        const table = document.querySelector("tbody");
        table.innerHTML = "";

        for (const [key, value] of Object.entries(data)) {
            const row = `
                <tr>
                    <td class="fw-bold text-center align-middle">${key}</td>
                    <td class="text-center">${value || "<i>Non spécifié</i>"}</td>
                </tr>`;
            table.innerHTML += row;
        }
    } else {
        alert("Erreur lors de la récupération du profil.");
    }
});
