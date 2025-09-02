document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("connexion-form");
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = form.querySelector("[name='email']").value;
    const password = form.querySelector("[name='password']").value;
    const nextParam = new URLSearchParams(location.search).get("next");
    const res = await fetch("/api/token/cookie/" + (nextParam ? `?next=${encodeURIComponent(nextParam)}` : ""), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ email, password, next: nextParam })
    });
    if (res.ok) {
      const data = await res.json().catch(()=>({}));
      const target = nextParam || data.redirect_to || "/profil/";
      window.location.replace(target);
    } else {
      const data = await res.json().catch(()=>({}));
      alert(data.error || data.detail || "Erreur");
    }
  });
});

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    input.type = input.type === "password" ? "text" : "password";
}