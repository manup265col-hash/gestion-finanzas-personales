# web/static/js/config.js — Anotado

Propósito

- Centraliza la base del API (`window.API_BASE`). Por defecto usa `window.location.origin` (same‑origin) para que el front y el back convivan en la misma app Heroku sin CORS.
- Permite override por query `?api=https://...` o por `localStorage` (clave `apiBaseOverride`).

Puntos clave

- `normalize(u)`: normaliza la URL (agrega https si falta y quita `/` final).
- `DEFAULT_SAME_ORIGIN = window.location.origin`.
- Orden de selección: query → localStorage → same-origin.
- Helpers `setApiBase` y `clearApiBaseOverride` para cambiar la base en tiempo de ejecución.

