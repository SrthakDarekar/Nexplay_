document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("joinForm");
    const passwordInput = document.getElementById("passwordField");
    const confirmPasswordInput = document.getElementById("confirmPasswordField");

    if (!form || !passwordInput || !confirmPasswordInput) {
        return;
    }

    form.addEventListener("submit", function (e) {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const pc=password.trim()
        // if((pc.length <= 8) && /[A-Z]/.test(pc) && )




        if (password !== confirmPassword) {
            e.preventDefault();

            if (window.Swal) {
                Swal.fire({
                    icon: "error",
                    title: "Passwords do not match",
                    text: "Please enter the same password in both fields."
                });
            } else {
                alert("Passwords do not match");
            }
        }

    });
});