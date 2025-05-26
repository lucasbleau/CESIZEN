document.addEventListener("DOMContentLoaded", function () {
    fetch("/api/accueil/")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("informations-content");
            data.forEach(info => {
                const card = `
                    <div class="col-md-6 mb-4">
                        <div class="card h-100 shadow">
                            <div class="card-body">
                                <h5 class="card-title">${info.titre}</h5>
                                ${info.sous_titre ? `<h6 class="card-subtitle mb-2 text-muted">${info.sous_titre}</h6>` : ''}
                                <p class="card-text">${info.contenu}</p>
                                <a href="#" class="card-link">Voir plus</a>
                            </div>
                        </div>
                    </div>
                `;
                container.innerHTML += card;
            });
        });
});
