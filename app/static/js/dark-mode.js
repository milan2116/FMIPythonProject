function toggleDarkMode() {
    const root = document.documentElement;
    if (root.getAttribute('data-theme') === 'dark') {
        root.removeAttribute('data-theme');
        localStorage.setItem('darkMode', 'disabled');
    } else {
        root.setAttribute('data-theme', 'dark');
        localStorage.setItem('darkMode', 'enabled');
    }
}

// Check for dark mode preference on page load
if (localStorage.getItem('darkMode') === 'enabled') {
    document.documentElement.setAttribute('data-theme', 'dark');
}