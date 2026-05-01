document.addEventListener('DOMContentLoaded', function() {
    // Lógica do Olhinho
    const togglers = document.querySelectorAll('.toggle-password');
    togglers.forEach(toggler => {
        toggler.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);
            
            if (input.type === 'password') {
                input.type = 'text';
                this.classList.replace('bi-eye-slash', 'bi-eye');
            } else {
                input.type = 'password';
                this.classList.replace('bi-eye', 'bi-eye-slash');
            }
        });
    });

    // Lógica do Semáforo (Integrada)
    const passwordInput = document.getElementById('password1');
    const feedbackText = document.getElementById('password-strength-text');

    if (passwordInput) {
        passwordInput.addEventListener('input', function() {
            const senha = this.value;
            let forca = 0;

            if (senha.length >= 8) forca += 1;
            if (/[A-Z]/.test(senha)) forca += 1;
            if (/[0-9]/.test(senha)) forca += 1;
            if (/[^A-Za-z0-9]/.test(senha)) forca += 1;

            // Reset
            if (senha.length === 0) {
                this.style.setProperty('border-color', '#e8e8e8', 'important');
                feedbackText.textContent = "";
            } else if (forca <= 1) {
                this.style.setProperty('border-color', '#ff4d4d', 'important'); // Vermelho
                feedbackText.textContent = "● Senha Fraca";
                feedbackText.style.color = "#ff4d4d";
            } else if (forca === 2) {
                this.style.setProperty('border-color', '#ffcc00', 'important'); // Amarelo
                feedbackText.textContent = "● Senha Mediana";
                feedbackText.style.color = "#ffcc00";
            } else {
                this.style.setProperty('border-color', '#27ae60', 'important'); // Verde
                feedbackText.textContent = "● Senha Forte";
                feedbackText.style.color = "#27ae60";
            }
        });
    }
});