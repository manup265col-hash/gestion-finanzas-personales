# web/static/js/index.js — Anotado

Resumen

- Maneja el login: lee email/password, valida, POST a `${API_BASE}/api/auth/login/`, guarda `access` en `sessionStorage` y redirige a `home.html`.

Detalles

- Formulario `#loginForm` escucha `submit` → `preventDefault()`.
- Mensajes de estado se muestran en `#message`.
- `fetch` con `Content-Type: application/json`.
- Si `response.ok`, guarda `authToken` y `username` y navega; si no, muestra error.

