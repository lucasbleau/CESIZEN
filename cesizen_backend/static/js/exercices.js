document.addEventListener("DOMContentLoaded", async () => {
    const container = document.getElementById("exercices-list");
    const loader = document.getElementById("loader");

    try {
        const res = await fetch("/api/exercices/", {
            method: "GET",
            credentials: "omit"
        });

        if (!res.ok) throw new Error("Erreur de chargement");

        const data = await res.json();

        loader.style.display = "none";

        if (data.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center text-muted">
                    Aucun exercice disponible pour le moment.
                </div>
            `;
            return;
        }

        data.forEach(ex => {
            const card = document.createElement("div");
            card.className = "col-12 col-md-6 col-lg-5 col-xl-4 d-flex justify-content-center";

            card.innerHTML = `
                <div class="card glass-card shadow-sm w-100">
                    <div class="card-body w-75 d-flex flex-column">
                        <h5 class="card-title">${ex.nom}</h5>
                        <p class="card-text flex-grow-1">Difficulté : ${ex.description}</p>
                        <a href="/exercices/${ex.id}/" class="btn">Lancer</a>
                    </div>
                </div>
            `;

            container.appendChild(card);
        });

    } catch (err) {
        loader.style.display = "none";
        console.error("Erreur :", err);
        container.innerHTML = `
            <div class="col-12 text-center text-danger">
                Une erreur est survenue lors du chargement des exercices.
            </div>
        `;
    }
});
