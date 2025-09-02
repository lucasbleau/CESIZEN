import { fetchWithAuth } from "./auth.js";

function getCookie(name){
  const m = document.cookie.match('(^|;)\\s*'+name+'=([^;]+)');
  return m ? decodeURIComponent(m.pop()) : "";
}
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("profil-edit-form");
  if (!form) return;
  form.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const data = {
      username: form.querySelector("[name='username']").value,
      email: form.querySelector("[name='email']").value
    };
    const res = await fetch("/api/profil/", {
      method: "PUT",
      headers: {
        "Content-Type":"application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      credentials: "include",
      body: JSON.stringify(data)
    });
    if (res.ok){
      const j = await res.json();
      alert("Profil mis à jour");
      location.href = "/profil/";
    } else {
      const err = await res.json().catch(()=>({}));
      alert("Erreur: "+JSON.stringify(err));
    }
  });
});

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
