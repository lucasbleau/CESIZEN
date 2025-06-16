document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("informations-content");
    const loader = document.getElementById("info-loading");

    loader.style.display = "block";

    fetch("/api/accueil/")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erreur lors de la récupération des données");
            }
            return response.json();
        })
        .then(data => {
            loader.style.display = "none";

            if (data.length === 0) {
                container.innerHTML = `
                    <div class="col-12 text-center">
                        <p class="text-muted">Aucune information disponible pour le moment.</p>
                    </div>
                `;
                return;
            }

            data.forEach(info => {
                const card = document.createElement('div');
                card.className = "col-md-6 mb-4";

                card.innerHTML = `
                    <div class="card h-100 shadow">
                        <div class="card-body">
                            <h5 class="card-title">${escapeHTML(info.titre)}</h5>
                            ${info.sous_titre ? `<h6 class="card-subtitle mb-2 text-muted">${escapeHTML(info.sous_titre)}</h6>` : ''}
                            <p class="card-text">${escapeHTML(info.contenu)}</p>
                        </div>
                    </div>
                `;

                container.appendChild(card);
            });
        })
        .catch(error => {
            loader.style.display = "none";
            container.innerHTML = `
                <div class="col-12 text-center text-danger">
                    <p>Impossible de charger les informations.</p>
                    <small>${error.message}</small>
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
