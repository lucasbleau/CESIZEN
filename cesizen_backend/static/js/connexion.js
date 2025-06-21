document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("connexion-form");
    const emailInput = form.querySelector("input[name='email']");
    const passwordInput = form.querySelector("input[name='password']");
    const rememberCheckbox = document.getElementById("remember-me");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
        const rememberMe = rememberCheckbox?.checked || false;

        const messageContainer = document.getElementById("message");
        messageContainer.innerHTML = "";

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
            errorDiv.className = "alert alert-danger text-center mt-2 mx-auto";
            errorDiv.textContent = data.detail || data.error || "Une erreur s’est produite.";
            messageContainer.appendChild(errorDiv);

            setTimeout(() => errorDiv.remove(), 5000);
        }
    });
});

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    input.type = input.type === "password" ? "text" : "password";
}