document.addEventListener('DOMContentLoaded', () => {
    const toggleIcons = document.querySelectorAll('.toggle-eye');

    toggleIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            const input = icon.parentElement.querySelector('input');

            if (input) {
                const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);

                icon.classList.toggle('fa-eye');
                icon.classList.toggle('fa-eye-slash');
            }
        });
    });
});