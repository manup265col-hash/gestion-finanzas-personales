# web/web/urls.py — Anotado

Objetivo: Definir las rutas públicas del proyecto: API de negocio, documentación y raíz que sirve el frontend estático.

Puntos clave

- Raíz `/`: redirige a `/static/index.html` para entregar el frontend estático.
- `api/`: incluye rutas de usuarios (login, me, etc.) y routers de ingresos/egresos/ahorros/prestamos.
- Documentación: `/schema/` (OpenAPI), `/docs/` (Swagger UI), `/redoc/` (ReDoc).
- Media en desarrollo/producción simple: `static(settings.MEDIA_URL, ...)` añade rutas de archivos subidos si aplica.

Flujo

1) Usuario abre `/` → se redirige a `/static/index.html` (front).
2) Front invoca `/api/...` para autenticación y datos.
3) Desarrollador consulta `/docs/` para ver y probar endpoints.

