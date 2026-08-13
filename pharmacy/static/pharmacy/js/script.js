document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.alert').forEach(el => {
    setTimeout(() => { el.style.opacity = '0'; el.style.transition = 'opacity .4s'; setTimeout(() => el.remove(), 500); }, 4500);
  });
});
function confirmDelete(item) { return confirm(`Delete this ${item}? This action cannot be undone.`); }
