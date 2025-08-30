# users/models.py — Anotado

Resumen

- `User` extiende `AbstractUser` para usar `email` como identificador y añadir campos (birthday, phone, country, profile_image).
- `profile_image` usa `ImageField` con `upload_to='profile_images/'`. Si hay `CLOUDINARY_URL`, el storage se cambia en tiempo de carga a Cloudinary (persistencia).
- Managers personalizados (`UserManager`) para crear usuarios y superusuarios con email.
- Modelos de soporte: `PasswordResetToken`, `PasswordResetCode`, `PendingSignup`.

Puntos clave

- Email como USERNAME_FIELD: login con email + password.
- Campo `profile_image`: admite `blank=True` y `null=True` y tiene default.
- Bloque final intenta forzar Cloudinary cuando está configurado.

