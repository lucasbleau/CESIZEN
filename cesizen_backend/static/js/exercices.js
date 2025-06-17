document.addEventListener("DOMContentLoaded", async () => {
    const loader = document.getElementById("loader");

    try {
        const res = await fetch("/api/exercices/", {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });

        const data = await res.json();

        if (res.ok) {
            loader.remove();

            const container = document.createElement("div");
            container.className = "row";

            data.forEach(exo => {
                const card = document.createElement("div");
                card.className = "col-md-6 mb-4";

                card.innerHTML = `
                    <div class="card shadow">
                        <div class="card-body">
                            <h5 class="card-title">${exo.nom}</h5>
                            <p class="card-text">${exo.description}</p>
                            <p><strong>Inspiration :</strong> ${exo.duree_inspiration}s</p>
                            <p><strong>Apnée :</strong> ${exo.duree_apnee}s</p>
                            <p><strong>Expiration :</strong> ${exo.duree_expiration}s</p>
                            <a href="/exercices/${exo.id}/" class="btn blue-bg-color text-light">Lancer</a>
                        </div>
                    </div>
                `;

                container.appendChild(card);
            });

            document.querySelector("main").appendChild(container);
        } else {
            loader.remove();
            alert("Impossible de récupérer les exercices.");
        }
    } catch (error) {
        loader.remove();
        console.error("Erreur lors du chargement des exercices :", error);
        alert("Erreur de connexion au serveur.");
    }
});
