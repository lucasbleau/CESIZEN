document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const emailInput = form.querySelector("input[name='email']");
    const usernameInput = form.querySelector("input[name='username']");
    const password1Input = form.querySelector("input[name='password1']");
    const password2Input = form.querySelector("input[name='password2']");
    const submitBtn = document.getElementById("submit-btn");

    form.addEventListener("submit", async (event) => {
        event.preventDefault(); // Empêche le rechargement

        const messageContainer = document.getElementById("message");
        if (messageContainer) messageContainer.remove();

        const email = emailInput.value.trim();
        const username = usernameInput.value.trim();
        const password1 = password1Input.value.trim();
        const password2 = password2Input.value.trim();

        const response = await fetch("/api/inscription/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCSRFToken(),
            },
            body: JSON.stringify({
                email,
                username,
                password1,
                password2,
            }),
        });

        const data = await response.json();

        if (response.ok) {
            // Succès : redirection
            window.location.href = "/";
        } else {
            // Affiche le message d'erreur
            const errorDiv = document.createElement("div");
            errorDiv.className = "text-center w-50 mb-3 alert alert-danger";
            errorDiv.id = "message";
            errorDiv.textContent = data.error || "Une erreur est survenue.";
            form.insertBefore(errorDiv, submitBtn);
        }
    });
});

function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        if (cookie.startsWith(name + "=")) {
            return cookie.split("=")[1];
        }
    }
    return "";
}
