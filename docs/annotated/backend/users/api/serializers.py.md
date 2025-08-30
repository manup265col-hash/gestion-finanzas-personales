# users/api/serializers.py — Anotado

Resumen

- `UserRegisterSerializer`: alta de usuario (escribe password, acepta `profile_image`).
- `UserSerializer`: respuesta básica de usuario, normaliza `profile_image` a URL absoluta si es posible.
- `UserUpdateSerializer`: actualización de datos (incluye `profile_image`) y también normaliza la URL en `to_representation`.

Por qué normalizar `profile_image`

- Cuando usas Cloudinary, `.url` ya es absoluta y pública → se devuelve tal cual.
- Cuando usas almacenamiento local/relative, se construye la URL absoluta con `request.build_absolute_uri(url)` si hay `request` en el contexto.

