from pathlib import Path
import os
from datetime import timedelta

# ======================================================
# RUTAS Y CONFIGURACIÓN BÁSICA
# ======================================================

# BASE_DIR: directorio raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================================
# CLAVES Y DEBUG
# ======================================================

# Clave secreta de Django
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-^j2&dyz6s@hy%b99mn9h@x59ebw%517mflsr^jne%n+ysql@&d"
)
# DEBUG: si es True, Django muestra errores detallados
# Por defecto activamos DEBUG en local para evitar problemas
# de archivos estáticos (Swagger UI) cuando no se ha hecho collectstatic.
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

# Hosts permitidos para este proyecto (producción)
ALLOWED_HOSTS = [
    "pagina-web-finansas-b6474cfcee14.herokuapp.com",  # Backend antiguo en Heroku
    "pagina-web-finansas.herokuapp.com",               # App Heroku actual
    "gestion-finanzas-personales.herokuapp.com",       # Nueva app Heroku
    ".herokuapp.com",                                  # Cualquier subdominio de Heroku
    "127.0.0.1",                                      # Local
    "localhost",                                      # Local
    "testserver",                                      # Cliente de pruebas de Django
]

# Si Heroku crea un host con sufijo aleatorio, inclúyelo dinámicamente
_heroku_app = os.environ.get('HEROKU_APP_NAME')
if _heroku_app:
    _host = f"{_heroku_app}.herokuapp.com"
    if _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)

# ======================================================
# APLICACIONES INSTALADAS
# ======================================================

INSTALLED_APPS = [
    # Apps predeterminadas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'cloudinary_storage',             # Storage de media en Cloudinary (antes de staticfiles)
    'django.contrib.staticfiles',
    
    # Terceros
    'drf_yasg',                      # Generación de documentación Swagger
    'rest_framework',                 # Django REST Framework
    'rest_framework_simplejwt.token_blacklist', # JWT blacklisting
    'django_filters',                 # Filtros para DRF
    'corsheaders',                    # Manejo de CORS
    'drf_spectacular',                # OpenAPI schema generation
    'drf_spectacular_sidecar',        # Swagger UI assets
    'cloudinary',
    
    # Apps locales
    'users', 
    'ingresos', 
    'egresos', 
    'ahorros', 
    'prestamos',
]

# ======================================================
# MIDDLEWARE
# ======================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',           # Seguridad general
    'whitenoise.middleware.WhiteNoiseMiddleware',             # Para servir archivos estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',    # Manejo de sesiones
    'corsheaders.middleware.CorsMiddleware',                  # CORS: debe ir antes de CommonMiddleware
    'django.middleware.common.CommonMiddleware',              # Funciones comunes (redirects, etc)
    'django.middleware.csrf.CsrfViewMiddleware',              # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Autenticación de usuarios
    'django.contrib.messages.middleware.MessageMiddleware',   # Mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Protección clickjacking
]

# ======================================================
# URLS Y TEMPLATES
# ======================================================

ROOT_URLCONF = 'web.urls'  # Archivo principal de URLs

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # Motor de templates
        'DIRS': [],   # Directorios adicionales de templates
        'APP_DIRS': True,  # Buscar templates dentro de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',   # Permite usar request en templates
                'django.contrib.auth.context_processors.auth',  # Datos de usuario en templates
                'django.contrib.messages.context_processors.messages', # Mensajes flash
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'  # Aplicación WSGI para despliegue

# ======================================================
# BASE DE DATOS
# ======================================================

import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,  # pooling en Heroku
    )
}

# ======================================================
# VALIDACIÓN DE CONTRASEÑAS
# ======================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'}, # Evita contraseñas similares al username
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},           # Longitud mínima
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},          # Evita contraseñas comunes
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},         # Evita contraseñas solo numéricas
]

# ======================================================
# INTERNACIONALIZACIÓN
# ======================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================================================
# DJANGO REST FRAMEWORK + JWT
# ======================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # Autenticación con JWT
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # Requiere login por defecto
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),  # Vida del token de acceso
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),     # Vida del refresh token
    "ROTATE_REFRESH_TOKENS": True,                   # Rotar refresh tokens al usar
    "BLACKLIST_AFTER_ROTATION": True,               # Añadir tokens rotados a blacklist
}

# ======================================================
# CORS
# ======================================================

# CORS: Revertido a back puro (sin orígenes externos específicos)
# Si necesitas habilitar orígenes en el futuro, define aquí la lista.
# CORS_ALLOWED_ORIGINS = []

# ======================================================
# ARCHIVOS ESTÁTICOS
# ======================================================

STATIC_URL = 'static/'                 # URL para servir archivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles' # Carpeta donde collectstatic pone los archivos

STATICFILES_DIRS = [
    BASE_DIR / "static",               # Carpeta adicional para buscar archivos estáticos
]

# ======================================================
# USER MODEL PERSONALIZADO
# ======================================================

AUTH_USER_MODEL = 'users.User'  # Modelo de usuario personalizado

# ======================================================
# EMAIL
# ======================================================

# Para desarrollo local (puedes activar si quieres depuración)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = 'webmaster@localhost'

# Para producción (Gmail SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')       # Usuario SMTP desde variable de entorno
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')   # Contraseña SMTP desde variable de entorno
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# ======================================================
# CAMPO POR DEFECTO PARA PK
# ======================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# En Heroku (DEBUG=False), usa /tmp para archivos de media (FS efímero pero escribible)
if not DEBUG and not os.environ.get('CLOUDINARY_URL'):
    # Solo usar FS efímero si NO usamos Cloudinary
    MEDIA_ROOT = Path('/tmp') / 'media'

# ======================================================
# SWAGGER / OpenAPI
# ======================================================

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer <token>"',
        }
    },
}

# ======================================================
# STATICFILES STORAGE (WhiteNoise)
# ======================================================
if not DEBUG:
    # En producción, para servir el frontend estático sin 'static' template tag
    # usamos la variante sin manifiesto para conservar nombres de archivos.
    # Así, referencias directas en HTML como /static/css/estilos.css no 404.
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Seguridad detrás de proxy (Heroku)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Confianza CSRF en dominios conocidos
CSRF_TRUSTED_ORIGINS = [
    'https://pagina-web-finansas.herokuapp.com',
    'https://pagina-web-finansas-b6474cfcee14.herokuapp.com',
    'https://gestion-finanzas-personales.herokuapp.com',
    'https://*.herokuapp.com',
]

if _heroku_app:
    _origin = f"https://{_heroku_app}.herokuapp.com"
    if _origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_origin)

## Mantener configuración de estáticos original (definida arriba)

# ======================================================
# MEDIA: Cloudinary en producción (si está configurado)
# ======================================================

# Si definimos CLOUDINARY_URL en variables de entorno, usamos Cloudinary para almacenar MEDIA
_cloudinary_url = os.environ.get("CLOUDINARY_URL")
if _cloudinary_url:
    try:
        # Insertar apps de cloudinary dinámicamente si no están ya
        if 'cloudinary_storage' not in INSTALLED_APPS:
            # antes de 'django.contrib.staticfiles' según recomendación
            idx = INSTALLED_APPS.index('django.contrib.staticfiles') if 'django.contrib.staticfiles' in INSTALLED_APPS else len(INSTALLED_APPS)
            INSTALLED_APPS.insert(idx, 'cloudinary_storage')
        if 'cloudinary' not in INSTALLED_APPS:
            INSTALLED_APPS.append('cloudinary')
    except Exception:
        # Si por alguna razón falla la inserción, aseguramos que existan igualmente
        INSTALLED_APPS = list(INSTALLED_APPS) + ['cloudinary_storage', 'cloudinary']

    # Storage por defecto para archivos subidos (MEDIA)
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    # Configuración opcional; si usas CLOUDINARY_URL no es necesario el dict
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }

## Eliminado: ajustes temporales de CORS/CSRF para integración con frontend

# Incluir el frontend estático (web-Front) para servirlo con WhiteNoise
try:
    STATICFILES_DIRS = list(STATICFILES_DIRS)
except NameError:
    STATICFILES_DIRS = []
# La carpeta web-Front está a nivel de proyecto (hermana de BASE_DIR)
from pathlib import Path as _Path
_frontend_dir = BASE_DIR.parent / 'web-Front'
if _frontend_dir.exists() and _frontend_dir not in STATICFILES_DIRS:
    STATICFILES_DIRS.append(_frontend_dir)

# Limpia entradas inexistentes para evitar warnings en collectstatic
try:
    STATICFILES_DIRS = [p for p in STATICFILES_DIRS if (p.exists() if isinstance(p, Path) else os.path.exists(p))]
except Exception:
    pass
