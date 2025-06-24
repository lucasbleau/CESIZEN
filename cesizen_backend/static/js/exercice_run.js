import { fetchWithAuth } from "./auth.js";
// import { hasAccessToken } from "./auth.js"; // décommente si tu l’utilises


let interval  = null;
let running   = false;
let startTime = null;
let exerciceId = null;
let sequence  = [];


document.addEventListener("DOMContentLoaded", async () => {
  console.log("⚡ JS exercice_run chargé");

  const container = document.querySelector(".exercice-container");
  if (!container) {
    console.error("❌ .exercice-container introuvable");
    return;
  }

  const circle   = document.getElementById("circle");
  const timerEl  = document.getElementById("timer");
  const phaseEl  = document.getElementById("phase");
  const startBtn = document.getElementById("start-btn");
  const stopBtn  = document.getElementById("stop-btn");


  try {
    const exId = container.dataset.exId;
    console.log("🔎 exId =", exId);

    const res = await fetchWithAuth(`/api/exercices/${exId}/`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const data = await res.json();
    exerciceId = data.id;

    sequence = [
      { phase: "Inspiration", duration: data.duree_inspiration, color: "#3498db", animate: true },
      { phase: "Apnée",       duration: data.duree_apnee,        color: "#f39c12", animate: false },
      { phase: "Expiration",  duration: data.duree_expiration,   color: "#e74c3c", animate: false }
    ];

  } catch (err) {
    phaseEl.textContent = "Impossible de charger l’exercice.";
    startBtn.disabled = true;
    console.error(err);
    return;
  }

  function updatePhase(p) {
    phaseEl.textContent          = p.phase;
    circle.style.backgroundColor = p.color;
    circle.classList.toggle("breathing", p.animate);
  }

  function startSequence(index = 0) {
    if (!running || index >= sequence.length) {
      stopSequence(true);         // terminé
      return;
    }

    const p = sequence[index];
    let t   = p.duration;

    if (t <= 0) {
      startSequence(index + 1);
      return;
    }

    updatePhase(p);
    timerEl.textContent = t;

    interval = setInterval(() => {
      t--;
      timerEl.textContent = t;
      if (t <= 0) {
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
    phaseEl.textContent = ended ? "Exercice terminé." : "Exercice interrompu.";

    if (startTime) {
      const dureeTotale = Math.floor((Date.now() - startTime) / 1000);
      enregistrerHistorique(exerciceId, dureeTotale);
      startTime = null;
    }
  }


  startBtn.addEventListener("click", () => {
    console.log("🟢 Démarrage exercice");
    if (!running) {
      running = true;
      startTime = Date.now();
      startSequence();
    }
  });

  stopBtn.addEventListener("click", () => stopSequence(false));
});


async function enregistrerHistorique(exId, dureeTotale) {
  if (!window.USER_AUTH /* || !hasAccessToken() */) {
    console.log("Invité : historique non enregistré");
    return;
  }

  console.log("Envoi historique :", exId, dureeTotale, "s");

  try {
    const res = await fetch("/api/historique/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
            exercice_id: exId,
            duree_totale: dureeTotale
        })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => res.statusText);
      console.error("Erreur API :", err);
    } else {
      console.log("Historique enregistré");
    }

  } catch (e) {
    console.error("❌ Erreur réseau :", e);
  }
}
