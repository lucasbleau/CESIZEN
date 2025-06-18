document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const emailInput = form.querySelector("input[name='email']");
    const passwordInput = form.querySelector("input[name='password']");
    const rememberCheckbox = document.getElementById("remember-me");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        const rememberMe = rememberCheckbox?.checked || false;

        const messageContainer = document.getElementById("message");
        if (messageContainer) messageContainer.remove();

        const response = await fetch("/api/token/cookie/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            credentials: "include",
            body: JSON.stringify({ email, password, remember: rememberMe }),
        });

        const data = await response.json();

        if (response.ok) {
            window.location.href = "/";
        } else {
            const errorDiv = document.createElement("div");
            errorDiv.className = "text-center mb-3 text-danger";
            errorDiv.id = "message";
            errorDiv.textContent = data.detail || data.error || "Une erreur s’est produite.";
            form.insertBefore(errorDiv, form.querySelector(".d-flex"));
        }
    });
});
