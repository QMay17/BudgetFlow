document.addEventListener('DOMContentLoaded', function() {
    // Password matching validation
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirm_password');

    if (passwordField && confirmPasswordField) {
        confirmPasswordField.addEventListener('input', function() {
            if (passwordField.value !== confirmPasswordField.value) {
                confirmPasswordField.setCustomValidity("Passwords do not match");
            } else {
                confirmPasswordField.setCustomValidity("");
            }
        });
    }

    // Auto-hide flash messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    if (messages.length > 0) {
        setTimeout(function() {
            messages.forEach(message => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                }, 300);
            });
        }, 5000);
    }
});