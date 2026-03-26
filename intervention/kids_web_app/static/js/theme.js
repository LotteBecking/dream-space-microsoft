/* theme.js — dark/light toggle with localStorage persistence */
(function () {
  var stored = localStorage.getItem('ds-theme');
  var preferred = stored
    || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  document.documentElement.setAttribute('data-theme', preferred);
})();

document.addEventListener('DOMContentLoaded', function () {
  var btn = document.getElementById('theme-toggle');
  if (!btn) return;

  function updateIcon(theme) {
    var moon = document.getElementById('icon-moon');
    var sun = document.getElementById('icon-sun');
    if (moon && sun) {
      moon.style.display = theme === 'dark' ? '' : 'none';
      sun.style.display = theme === 'light' ? '' : 'none';
    }
    btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  }

  var current = document.documentElement.getAttribute('data-theme') || 'dark';
  updateIcon(current);

  btn.addEventListener('click', function () {
    var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('ds-theme', next);
    updateIcon(next);
  });
});
