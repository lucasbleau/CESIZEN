document.addEventListener("DOMContentLoaded", () => {
    const circle = document.getElementById("circle");
    const timerEl = document.getElementById("timer");
    const phaseEl = document.getElementById("phase");
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");

    let sequence = [];
    let interval = null;
    let running = false;
    let startTime = null;

    const exerciceData = JSON.parse(document.getElementById("exercice-data").textContent);
    const exerciceId = exerciceData.id;

    sequence = [
        { phase: "Inspiration", duration: exerciceData.duree_inspiration, color: "#3498db", animate: true },
        { phase: "Apnée",        duration: exerciceData.duree_apnee,        color: "#f39c12", animate: false },
        { phase: "Expiration",   duration: exerciceData.duree_expiration,   color: "#e74c3c", animate: false },
    ];

    function updatePhase(phase) {
        phaseEl.textContent = phase.phase;
        circle.style.backgroundColor = phase.color;

        if (phase.animate) {
            circle.classList.add("breathing");
        } else {
            circle.classList.remove("breathing");
        }
    }

    function startSequence(index = 0) {
        if (!running || index >= sequence.length) {
            stopSequence(true);
            return;
        }

        const phase = sequence[index];
        let time = phase.duration;

        updatePhase(phase);
        timerEl.textContent = time;

        interval = setInterval(() => {
            time--;
            timerEl.textContent = time;
            if (time <= 0) {
                clearInterval(interval);
                startSequence(index + 1);
            }
        }, 1000);
    }

    function stopSequence(ended = false) {
        running = false;
        clearInterval(interval);
        timerEl.textContent = "0";
        circle.classList.remove("breathing");
        circle.style.backgroundColor = "#85c1e9";

        if (ended) {
            phaseEl.textContent = "Exercice terminé.";
        } else {
            phaseEl.textContent = "Exercice interrompu.";
        }

        if (startTime) {
            const dureeTotale = Math.floor((Date.now() - startTime) / 1000);
            enregistrerHistorique(exerciceId, dureeTotale);
            startTime = null;
        }
    }

    startBtn.addEventListener("click", () => {
        if (!running) {
            running = true;
            startTime = Date.now();
            startSequence();
        }
    });

    stopBtn.addEventListener("click", () => {
        stopSequence(false);
    });
});

async function enregistrerHistorique(exerciceId, dureeTotale) {
    try {
        const response = await fetch("/api/historique/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: "include", 
            body: JSON.stringify({
                exercice_id: exerciceId,
                duree_totale: dureeTotale
            }),
        });

        if (response.status === 401) {
            console.warn("Utilisateur non connecté : historique non enregistré.");
            return;
        }

        if (!response.ok) {
            const errorData = await response.json();
            console.error("Erreur API :", errorData);
        } else {
            console.log("Historique enregistré avec succès !");
        }

    } catch (error) {
        console.error("Erreur réseau :", error);
    }
}
