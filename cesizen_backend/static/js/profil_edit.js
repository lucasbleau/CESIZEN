import { fetchWithAuth } from "./auth.js";

document.addEventListener("DOMContentLoaded", async () => {
    const tbody = document.getElementById("profil-edit-table");
    const form = document.getElementById("profil-edit-form");

    const res = await fetchWithAuth("/api/profil/");
    if (!res.ok) {
        tbody.innerHTML = `<tr><td colspan="2" class="text-danger text-center">Erreur de chargement.</td></tr>`;
        return;
    }

    const data = await res.json();

    const editableFields = {
        "username": "Nom d'utilisateur",
        "email": "Email",
        "first_name": "Prénom",
        "last_name": "Nom"
    };

    tbody.innerHTML = "";
    for (const key in editableFields) {
        const label = editableFields[key];
        const value = data[key] || "";
        tbody.innerHTML += `
            <tr>
                <td class="fw-bold text-center align-middle">${label}</td>
                <td class="text-center">
                    <input type="text" class="form-control" name="${key}" value="${value}">
                </td>
            </tr>
        `;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const body = {};
        for (const [key, value] of formData.entries()) {
            body[key] = value.trim();
        }

        const updateRes = await fetchWithAuth("/api/profil/", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });

        if (!updateRes.ok) {
            const errorData = await updateRes.json();
            console.error("Échec de la mise à jour :", errorData);

            let msg = "Échec de la mise à jour du profil :\n";
            for (const [field, errors] of Object.entries(errorData)) {
                msg += `• ${field} : ${errors.join(", ")}\n`;
            }
            alert(msg);
            return;
        }

        const successDiv = document.createElement("div");
        successDiv.className = "alert alert-success text-center mt-3";
        successDiv.textContent = "✅ Changements enregistrés avec succès.";
        form.appendChild(successDiv);

        setTimeout(() => {
            window.location.href = "/profil/";
        }, 2000);
    });
});
