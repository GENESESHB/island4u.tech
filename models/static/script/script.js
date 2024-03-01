// Ensure the modals are hidden initially
document.addEventListener('DOMContentLoaded', function () {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(function (modal) {
        modal.style.display = 'none';
    });
});

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'block';
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

