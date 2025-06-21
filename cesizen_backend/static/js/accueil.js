document.addEventListener("DOMContentLoaded", () => {
    const carouselInner = document.querySelector(".carousel-inner");
    const loader = document.getElementById("info-loading");

    loader.style.display = "block";

    fetch("/api/accueil/", {
        method: "GET",
        credentials: "omit",
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erreur lors de la récupération des données");
            }
            return response.json();
        })
        .then(data => {
            loader.style.display = "none";

            if (!data || data.length === 0) {
                carouselInner.innerHTML = `
                    <div class="carousel-item active">
                        <div class="glass-card text-center mx-auto" style="max-width: 600px;">
                            <p class="text-muted">Aucune information disponible pour le moment.</p>
                        </div>
                    </div>
                `;
                return;
            }

            data.forEach((info, index) => {
                const item = document.createElement("div");
                item.className = `carousel-item${index === 0 ? " active" : ""}`;

                item.innerHTML = `
                    <div class="glass-card text-center mx-auto" style="max-width: 600px;">
                        <h5>${escapeHTML(info.titre)}</h5>
                        ${info.sous_titre ? `<h6 class="mb-2 text-muted">${escapeHTML(info.sous_titre)}</h6>` : ""}
                        <p>${escapeHTML(info.contenu)}</p>
                    </div>
                `;

                carouselInner.appendChild(item);
            });
        })
        .catch(error => {
            loader.style.display = "none";
            carouselInner.innerHTML = `
                <div class="carousel-item active">
                    <div class="glass-card text-center mx-auto" style="max-width: 600px;">
                        <p class="text-danger">Impossible de charger les informations.</p>
                        <small>${escapeHTML(error.message)}</small>
                    </div>
                </div>
            `;
        });
});

function escapeHTML(str) {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
