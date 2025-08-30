# web/static/js/profile.js — Anotado

Resumen

- Al cargar: requiere `authToken`; si no existe, redirige a `index.html`.
- Carga perfil con `GET /api/auth/me/` y setea inputs + imagen.
- Edición: habilita inputs; `Save` abre modal de confirmación.
- Guardar: `PUT /api/auth/me/` con `FormData` (incluye `profile_image`).
- Imagen: intenta URL directa con cache‑busting → si falla, `fetch` autenticado como `blob` → si no, fallback a cache `localStorage` por `userId`.
- Vista previa local al seleccionar archivo (FileReader) y cache local por usuario.

