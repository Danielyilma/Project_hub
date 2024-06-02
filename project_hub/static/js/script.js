const bellBtn = document.getElementById('bell-btn');
const notification = document.getElementById('notification');

bellBtn.addEventListener('click', () => {
    notification.style.display = 'block';
    document.addEventListener('click', handleOutsideClick);
});

function handleOutsideClick(event) {
    if (!notification.contains(event.target) && event.target !== bellBtn) {
        notification.style.display = 'none';
        document.removeEventListener('click', handleOutsideClick);
    }
}