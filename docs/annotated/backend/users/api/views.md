# users/api/views.py — Anotado

Resumen del flujo

- Vistas basadas en clases para: registro, login JWT, refresco, obtención/actualización de perfil (`/api/auth/me/`), logout, reset de contraseña y aprobación de signup.
- Usan DRF (serializers + permisos) y SimpleJWT para emisión/validación de tokens.
- Las respuestas de perfil incluyen `profile_image` normalizado (ver serializers).

Puntos clave a revisar en el archivo real

- LoginView: valida credenciales y devuelve `access` (JWT).
- UserInfoView / userView: usan `IsAuthenticated` y devuelven datos del usuario.
- PUT en `me/`: recibe `multipart/form-data` para actualizar datos y `profile_image`.
- Reset password flow: endpoints `password-reset`, `password-verify`, `password-reset-confirm`.

