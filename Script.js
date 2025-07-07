const secciones = document.querySelectorAll('.seccion');

// Detecta si una sección está en el viewport
function estaVisible(seccion) {
    const rect = seccion.getBoundingClientRect();
    const ventanaAltura = window.innerHeight || document.documentElement.clientHeight;
    return (
        rect.top < ventanaAltura * 0.85 &&
        rect.bottom > 0
    );
}

function actualizarAnimaciones() {
    secciones.forEach(seccion => {
        if (estaVisible(seccion)) {
            seccion.classList.add('visible');
        } else {
            seccion.classList.remove('visible'); // Reinicia si se sale de la vista
        }
    });
}

// Vuelve a evaluar cada vez que se hace scroll o al cargar
window.addEventListener('scroll', actualizarAnimaciones);
window.addEventListener('load', actualizarAnimaciones);
