document.addEventListener("DOMContentLoaded", () => {
    const circle = document.getElementById("circle");
    const timerEl = document.getElementById("timer");
    const phaseEl = document.getElementById("phase");
    const startBtn = document.getElementById("start-btn");
    const stopBtn = document.getElementById("stop-btn");

    let sequence = [];
    let interval = null;
    let running = false;

    const urlParts = window.location.pathname.split("/");
    const exerciceId = urlParts[urlParts.length - 2]; 

    fetch(`/api/exercices/`)
        .then(res => res.json())
        .then(data => {
            const exercice = data.find(e => e.id === parseInt(exerciceId));
            if (!exercice) throw new Error("Exercice non trouvé.");

            sequence = [
                { phase: "Inspiration", duration: exercice.duree_inspiration, color: "#3498db" },
                { phase: "Apnée", duration: exercice.duree_apnee, color: "#f39c12" },
                { phase: "Expiration", duration: exercice.duree_expiration, color: "#e74c3c" },
            ];
        })
        .catch(err => {
            alert("Erreur de chargement de l'exercice.");
            console.error(err);
        });

    function updatePhase(phase) {
        phaseEl.textContent = phase.phase;
        circle.style.backgroundColor = phase.color;
    }

    function startSequence(index = 0) {
        if (!running || index >= sequence.length) {
            stopSequence();
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

    function stopSequence() {
        running = false;
        clearInterval(interval);
        phaseEl.textContent = "Exercice interrompu.";
        timerEl.textContent = "0";
        circle.style.backgroundColor = "#85c1e9";
    }

    startBtn.addEventListener("click", () => {
        if (!running) {
            running = true;
            startSequence();
        }
    });

    stopBtn.addEventListener("click", () => {
        stopSequence();
    });
});
