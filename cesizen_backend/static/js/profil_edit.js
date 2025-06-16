import { fetchWithAuth } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    const res = await fetchWithAuth("/api/profil/");
    const data = await res.json();

    if (res.ok) {
        const tbody = document.querySelector("tbody");
        tbody.innerHTML = "";

        for (const [key, value] of Object.entries(data)) {
            const row = `
                <tr>
                    <td class="fw-bold text-center align-middle">${key}</td>
                    <td class="text-center">
                        <input type="text" class="form-control" name="${key}" value="${value || ''}">
                    </td>
                </tr>`;
            tbody.innerHTML += row;
        }

        const form = document.querySelector("form");
        form.addEventListener("submit", async (e) => {
            e.preventDefault();

            const formData = new FormData(form);
            const body = {};

            for (const [key, value] of formData.entries()) {
                body[key] = value;
            }

            console.log("Données envoyées :", body); 

            const updateRes = await fetchWithAuth("/api/profil/", {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(body)
            });

            if (updateRes.ok) {
                window.location.href = "/profil/";
            } else {
                alert("Échec de la mise à jour du profil.");
            }
        });

    } else {
        alert("Impossible de charger le profil.");
    }
});
