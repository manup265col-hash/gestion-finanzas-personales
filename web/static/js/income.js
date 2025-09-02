// Esperamos a que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', async () => {
    
    // Recuperamos el token de autenticación guardado en sessionStorage
    const token = sessionStorage.getItem('authToken');

    // Si no hay token, redirigimos al login (index.html)
    if (!token) { 
        window.location.href = 'index.html'; 
        return; 
    }

    // Base de la API, la tomamos de config.js o del origen actual de la página
    const API_BASE = window.API_BASE || window.location.origin;

    // Obtenemos referencias a los elementos del DOM
    const nameEl = document.getElementById('incomeUsername');       // Nombre del usuario
    const iconEl = document.getElementById('walletProfileIcon');    // Ícono por defecto (bi-person)
    const imgEl  = document.getElementById('walletProfileImage');   // Imagen de perfil

    // Función auxiliar que transforma la ruta de la imagen en una URL válida
    const resolveImageUrl = (raw) => {
        if (!raw) return null;              // Si no hay valor, devolvemos null
        const s = String(raw).trim();       // Convertimos a string y quitamos espacios
        if (!s) return null;                // Si queda vacío, null
        if (/^https?:\/\//i.test(s)) return s; // Si ya es una URL absoluta (http/https), la devolvemos
        const path = s.startsWith('/') ? s : `/${s}`; // Si no, aseguramos que comience con "/"
        return `${API_BASE}${path}`;        // Concatenamos con la base de la API
    };

    try {
        // Llamamos al endpoint de perfil del usuario
        const res = await fetch(`${API_BASE}/api/auth/me/`, {
            headers: {
                'Content-Type': 'application/json',   // Cabecera para JSON
                'Authorization': 'Bearer ' + token,   // Token de autenticación
            },
        });

        // Si la respuesta no es correcta (401 o error), lanzamos excepción
        if (!res.ok) throw new Error('No autorizado');

        // Parseamos el JSON con los datos del usuario
        const data = await res.json();

        // Colocamos el nombre o email en el elemento correspondiente
        if (nameEl) {
            nameEl.textContent = data.first_name || data.email || 'Usuario';
        }

        // Resolvemos la URL de la imagen de perfil
        const url = resolveImageUrl(data && data.profile_image);

        // Si hay imagen y elementos válidos
        if (url && imgEl && iconEl) {
            // Cuando la imagen carga correctamente, la mostramos y ocultamos el ícono
            imgEl.onload = () => { 
                imgEl.style.display = 'block'; 
                iconEl.style.display = 'none'; 
            };
            // Si ocurre error al cargar, ocultamos la imagen y mostramos el ícono
            imgEl.onerror = () => { 
                imgEl.style.display = 'none'; 
                iconEl.style.display = 'block'; 
            };
            // Asignamos la URL con un parámetro de tiempo para evitar usar caché
            imgEl.src = url + (url.includes('?') ? `&t=${Date.now()}` : `?t=${Date.now()}`);
        }
    } catch (e) {
        // Si ocurre algún error, forzamos login
        window.location.href = 'index.html';
    }

    // --- Comportamiento de Tabs ---
    // Seleccionamos los botones de pestañas
    const tabs = document.querySelectorAll('.tab-btn');

    // Añadimos evento de click a cada pestaña
    tabs.forEach(btn => {
        btn.addEventListener('click', () => {
            // Quitamos la clase activa de todas las pestañas
            tabs.forEach(b => b.classList.remove('active'));
            // Marcamos la pestaña clicada como activa
            btn.classList.add('active');
            // Buscamos la vista correspondiente a la pestaña
            const target = document.querySelector(btn.dataset.target);
            // Ocultamos todas las vistas
            document.querySelectorAll('.tab-view').forEach(v => v.style.display = 'none');
            // Mostramos solo la vista seleccionada
            if (target) target.style.display = 'block';
        });
    });

    // Por defecto activamos la primera pestaña si existe
    const first = document.querySelector('.tab-btn');
    if (first) first.click();
});
