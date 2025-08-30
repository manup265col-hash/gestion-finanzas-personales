# web/web/settings.py — Anotado

Objetivo: Configurar Django para producción en Heroku (mismo dominio para API y frontend estático), JWT, Swagger, Cloudinary opcional, y WhiteNoise para estáticos.

Secciones clave explicadas

- BASE_DIR y DEBUG: ruta base del proyecto y modo debug por variable `DJANGO_DEBUG`.
- ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS: incluye tus dominios Heroku y wildcard `.herokuapp.com` para cubrir sufijos aleatorios.
- INSTALLED_APPS: Django, DRF, JWT blacklist, filtros, CORS (sin usar en producción same‑origin), drf-spectacular + sidecar, cloudinary_storage.
- MIDDLEWARE: WhiteNoise para estáticos, corsheaders (no impacta en same-origin), seguridad/sesión/CSRF.
- DATABASES: `dj_database_url.parse` toma `DATABASE_URL` (Heroku Postgres) o local sqlite.
- REST_FRAMEWORK + SIMPLE_JWT: autenticación JWT, permisos por defecto `IsAuthenticated` y lifetimes.
- Staticfiles: `STATIC_URL`, `STATIC_ROOT`; storage WhiteNoise comprimido sin manifiesto para mantener nombres originales; `WHITENOISE_USE_FINDERS=True` permite servir desde finders aun si no hay archivos en `STATIC_ROOT`.
- Media/Cloudinary: si `CLOUDINARY_URL` está definida, usar `MediaCloudinaryStorage` para persistencia de imágenes de perfil.
- Swagger: seguridad tipo Bearer y endpoints documentados.

Notas de diseño

- Same‑origin: el front se sirve desde `/static/...` y consume `/api/...` en el mismo host Heroku (evita CORS en producción).
- WhiteNoise sin manifiesto: facilita servir HTML/CSS/JS estáticos con rutas fijas.
- Cloudinary: recomendado para imágenes de usuario (Heroku FS es efímero). Con solo `CLOUDINARY_URL`, el modelo y settings adaptan el storage.

Puntos de referencia en código real

- ALLOWED_HOSTS: contiene `.herokuapp.com` y añade dinámicamente `{HEROKU_APP_NAME}.herokuapp.com` si se define la variable.
- CSRF_TRUSTED_ORIGINS: incluye `https://*.herokuapp.com` para evitar problemas de CSRF en producción.
- STATICFILES STORAGE: `whitenoise.storage.CompressedStaticFilesStorage` y `WHITENOISE_USE_FINDERS=True`.
- MEDIA_ROOT: usa `/tmp/media` cuando `DEBUG=False` y no hay Cloudinary (solo para testing simple; en prod usar Cloudinary).

