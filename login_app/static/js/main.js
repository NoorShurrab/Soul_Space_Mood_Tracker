// document.addEventListener('DOMContentLoaded', () => {
//     const passwordInput = document.getElementById('password');
//     const toggleEye = document.getElementById('toggleEye');

//     if (toggleEye && passwordInput) {
//         toggleEye.addEventListener('click', () => {
//             // التبديل بين نوع الحقل text و password
//             const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
//             passwordInput.setAttribute('type', type);
            
//             // تبديل شكل الأيقونة لتصبح مشطوبة عند الإظهار وعادية عند الإخفاء
//             toggleEye.classList.toggle('fa-eye');
//             toggleEye.classList.toggle('fa-eye-slash');
//         });
//     }
// });


document.addEventListener('DOMContentLoaded', () => {
    const toggleIcons = document.querySelectorAll('.toggle-eye');

    toggleIcons.forEach(icon => {
        icon.addEventListener('click', () => {
            const input = icon.parentElement.querySelector('input');

            if (input) {
                // التبديل بين نوع الحقل
                const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);

                // التبديل بين شكل العين المشطوبة والمفتوحة
                icon.classList.toggle('fa-eye');
                icon.classList.toggle('fa-eye-slash');
            }
        });
    });
});