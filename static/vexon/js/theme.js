let currentTheme = 'light';

function setTheme(theme) {
    const isDark = theme === 'dark';        

    // Activar/desactivar estilos según el tema
    const mainDark = document.getElementById('main-dark');
    const menuDark = document.getElementById('menu-dark');
    const mainLight = document.getElementById('main-light');
    const menuLight = document.getElementById('menu-light');        

    // Verificar que los elementos existen antes de modificarlos
    if (mainDark) mainDark.disabled = !isDark;
    if (menuDark) menuDark.disabled = !isDark;
    if (mainLight) mainLight.disabled = isDark;
    if (menuLight) menuLight.disabled = isDark;

    // Guardar tema actual en variable y en localStorage
    currentTheme = theme;
    localStorage.setItem('theme', theme);
    
    // Añadir clase al body para CSS adicional
    document.body.className = theme + '-theme';

    // Actualizar el icono del botón con emojis
    const themeIcon = document.getElementById('theme-icon');
    if (themeIcon) {
        themeIcon.textContent = isDark ? '☀️' : '🌙';
    }
}

// Alternar entre temas
function toggleTheme() {
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
}

// Aplicar tema inicial y configurar event listeners al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    // Recuperar tema desde localStorage o usar 'light' por defecto
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    // Configurar event listener para el botón de cambio de tema usando ID
    const themeButton = document.getElementById('theme-toggle-btn');
    
    if (themeButton) {
        themeButton.addEventListener('click', function(event) {
            // Prevenir comportamientos por defecto y propagación
            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();
            
            console.log('Botón de tema clickeado por ID');
            
            // Cambiar tema
            toggleTheme();
        });
        console.log('Botón de tema configurado correctamente');
    } else {
        console.warn('Botón de cambio de tema no encontrado con ID #theme-toggle-btn');
    }
});