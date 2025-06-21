document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const emailInput = form.querySelector("input[name='email']");
    const usernameInput = form.querySelector("input[name='username']");
    const password1Input = form.querySelector("input[name='password1']");
    const password2Input = form.querySelector("input[name='password2']");
    const submitBtn = document.getElementById("submit-btn");

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

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
            window.location.href = "/";
        } else {
            const errorDiv = document.createElement("div");
            errorDiv.className = "text-center w-50 mb-3 alert alert-danger w-75 mx-auto";
            errorDiv.id = "message";
            errorDiv.textContent = data.error || "Une erreur est survenue.";
            form.insertBefore(errorDiv, submitBtn);
            setTimeout(() => {
                errorDiv.remove();
            }, 5000);
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


document.addEventListener("DOMContentLoaded", function () {
    const passwordInput = document.getElementById("password1");
    const confirmPasswordInput = document.getElementById("password2");
    const emailInput = document.getElementById("email");
    const usernameInput = document.getElementById("username");
    const submitButton = document.getElementById("submit-btn");
    const criteria = {
        length: document.getElementById("criteria-length"),
        lowercase: document.getElementById("criteria-lowercase"),
        uppercase: document.getElementById("criteria-uppercase"),
        special: document.getElementById("criteria-special")
    };

    function validatePassword() {
        const password = passwordInput.value.trim();
        const email = emailInput.value.trim();
        const username = usernameInput.value.trim();

        const isLongEnough = password.length >= 12;
        const hasLowercase = /[a-z]/.test(password);
        const hasUppercase = /[A-Z]/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        const allFieldsFilled = email && username && password && confirmPasswordInput.value;

        criteria.length.classList.toggle("valid", isLongEnough);
        criteria.length.classList.toggle("invalid", !isLongEnough);

        criteria.lowercase.classList.toggle("valid", hasLowercase);
        criteria.lowercase.classList.toggle("invalid", !hasLowercase);

        criteria.uppercase.classList.toggle("valid", hasUppercase);
        criteria.uppercase.classList.toggle("invalid", !hasUppercase);

        criteria.special.classList.toggle("valid", hasSpecialChar);
        criteria.special.classList.toggle("invalid", !hasSpecialChar);

        const allValid = isLongEnough && hasLowercase && hasUppercase && hasSpecialChar && allFieldsFilled;

        submitButton.disabled = !allValid;
    }

    [passwordInput, confirmPasswordInput, emailInput, usernameInput].forEach(input => {
        input.addEventListener("input", validatePassword);
    });

    validatePassword();
});

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    input.type = input.type === "password" ? "text" : "password";
}