import { startAutoLogout } from "./auth.js";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const emailInput = form.querySelector("input[name='email']");
    const passwordInput = form.querySelector("input[name='password']");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();

        const messageContainer = document.getElementById("message");
        if (messageContainer) messageContainer.remove();

        const response = await fetch("/api/token/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem("access", data.access);
            localStorage.setItem("refresh", data.refresh);

            startAutoLogout(data.access);

            window.location.href = "/";
        } else {
            const errorDiv = document.createElement("div");
            errorDiv.className = "text-center mb-3 text-danger";
            errorDiv.id = "message";
            errorDiv.textContent = data.detail || "Une erreur s’est produite.";
            form.insertBefore(errorDiv, form.querySelector(".d-flex"));
        }
    });
});