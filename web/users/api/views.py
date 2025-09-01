# -*- coding: latin-1 -*-
# Importamos librerÃƒÆ’Ã‚Â­as necesarias
import random  # Para generar cÃƒÆ’Ã‚Â³digos aleatorios de recuperaciÃƒÆ’Ã‚Â³n
from rest_framework import status, permissions  # Para respuestas HTTP y permisos
from rest_framework.views import APIView  # Para crear vistas basadas en clases
from rest_framework.response import Response  # Para devolver respuestas JSON
from users.api.serializers import (
    UserRegisterSerializer, UserUpdateSerializer,
    PasswordResetRequestSerializer, PasswordResetVerifySerializer,
    PasswordResetConfirmSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny  # Permisos para vistas
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from users.models import User, PasswordResetToken  # Modelos de usuario y token
from django.core.mail import send_mail  # Para enviar emails
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings  # Para acceder a configuraciones (ej. email)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser  # Necesario para manejar imÃƒÆ’Ã‚Â¡genes

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .utils import approve_signup_and_send_code
from django.core.files.storage import default_storage

# -----------------------------------------------------------
# VISTA DE REGISTRO DE USUARIO
# -----------------------------------------------------------
class RegisterView(APIView):
    """
    Vista para registrar nuevos usuarios.
    Permite subir imagen de perfil usando multipart/form-data.
    """
    permission_classes = [AllowAny]  # Cualquiera puede acceder
    parser_classes = [MultiPartParser, FormParser]  # Soporte para envÃƒÆ’Ã‚Â­o de archivos e imÃƒÆ’Ã‚Â¡genes

    @swagger_auto_schema(
        operation_summary='Registro de usuario',
        tags=['Auth'],
        operation_description='Crea un usuario nuevo. EnvÃƒÂ­a multipart/form-data si incluye profile_image, o JSON si no envÃƒÂ­a archivo.',
        consumes=['multipart/form-data', 'application/json'],
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description='Correo'),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description='ContraseÃƒÂ±a'),
            openapi.Parameter('birthday', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True, description='YYYY-MM-DD'),
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter('phone', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('country', openapi.IN_FORM, type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('profile_image', openapi.IN_FORM, type=openapi.TYPE_FILE, required=False)
        ],
        responses={
            201: openapi.Response(
                description='Usuario creado',
                examples={'application/json': {'id': 1, 'email': 'user@mail.com'}}
            )
        }
    )
    def post(self, request):
        """
        Maneja la solicitud POST para registrar un nuevo usuario.
        """
        serializer = UserRegisterSerializer(data=request.data, context={'request': request})  # Crea serializer con datos recibidos
        if serializer.is_valid(raise_exception=True):  # Valida datos, lanza excepciÃƒÆ’Ã‚Â³n si no son vÃƒÆ’Ã‚Â¡lidos
            serializer.save()  # Guarda el usuario en la base de datos
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Responde con datos del usuario
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------
# VISTA DE PERFIL DE USUARIO
# -----------------------------------------------------------
class userView(APIView):
    """
    Vista para obtener y actualizar informaciÃƒÆ’Ã‚Â³n del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]  # Solo usuarios logueados
    parser_classes = [MultiPartParser, FormParser]  # Soporta envÃƒÂ­o de archivos para profile_image

    @swagger_auto_schema(operation_summary='Perfil del usuario (detalle)', tags=['Usuarios'],
                        responses={200: openapi.Response('OK', examples={'application/json': {
                            'id': 1,
                            'email': 'user@mail.com',
                            'birthday': '2000-01-01',
                            'first_name': 'Nelson',
                            'last_name': 'Giraldo',
                            'phone': '3000000000',
                            'country': 'CO',
                            'profile_image': None
                        }})})
    def get(self, request):
        """
        Devuelve informaciÃƒÆ’Ã‚Â³n del usuario autenticado.
        """
        serializer = UserRegisterSerializer(request.user, context={'request': request})  # Serializa datos del usuario
        return Response(serializer.data)  # Devuelve datos serializados en formato JSON

    @swagger_auto_schema(operation_summary='Actualizar perfil de usuario', tags=['Usuarios'],
                         request_body=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                              'first_name': openapi.Schema(type=openapi.TYPE_STRING, example='Nelson'),
                              'last_name': openapi.Schema(type=openapi.TYPE_STRING, example='Giraldo'),
                              'birthday': openapi.Schema(type=openapi.TYPE_STRING, example='2000-01-01'),
                              'phone': openapi.Schema(type=openapi.TYPE_STRING, example='3000000000'),
                              'country': openapi.Schema(type=openapi.TYPE_STRING, example='CO'),
                              'profile_image': openapi.Schema(type=openapi.TYPE_STRING, format='binary')
                            }
                         ))
    def put(self, request):
        """
        Actualiza datos del usuario, incluyendo imagen de perfil.
        """
        user = User.objects.get(id=request.user.id)  # Busca el usuario autenticado en BD
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # Permite actualizaciÃƒÆ’Ã‚Â³n parcial
        if serializer.is_valid(raise_exception=True):  # Valida datos enviados
            serializer.save()  # Guarda cambios en la base de datos
            return Response(UserUpdateSerializer(user, context={'request': request}).data)  # Devuelve datos actualizados con URL absoluta
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------
# DEBUG: INFO DE STORAGE
# -----------------------------------------------------------
"""
Nota: Se eliminaron las vistas de diagnÃ³stico usadas durante la integraciÃ³n
de Cloudinary y el debug de despliegue para mantener el cÃ³digo limpio.
"""


# -----------------------------------------------------------
# SOLICITUD DE RESET DE CONTRASEÃƒÆ’Ã¢â‚¬ËœA
# -----------------------------------------------------------
class PasswordResetRequestView(APIView):
    """
    EnvÃƒÆ’Ã‚Â­a un cÃƒÆ’Ã‚Â³digo al correo para poder restablecer la contraseÃƒÆ’Ã‚Â±a.
    """
    permission_classes = [AllowAny]  # Cualquiera puede solicitarlo

    @swagger_auto_schema(operation_summary='Solicitar codigo de reseteo', tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email'],
            properties={'email': openapi.Schema(type=openapi.TYPE_STRING, example='user@mail.com')}
        ),
        responses={200: openapi.Response('OK', examples={'application/json': {'detail': 'Codigo enviado'}})}
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)  # Serializa datos recibidos
        serializer.is_valid(raise_exception=True)  # Valida datos

        email = serializer.validated_data["email"]  # Obtiene email
        try:
            user = User.objects.get(email=email)  # Busca usuario por email
        except User.DoesNotExist:
            return Response({"error": "No existe un usuario con ese correo."}, status=404)

        # Genera cÃƒÆ’Ã‚Â³digo aleatorio de 6 dÃƒÆ’Ã‚Â­gitos
        token = str(random.randint(10000000, 99999999))

        # Crea registro de token para ese usuario
        PasswordResetToken.objects.create(user=user, token=token)
        
        # Enviar correo con plantilla (texto + HTML)
        # Envia correo real usando SMTP configurado en settings.py
        send_mail(
            subject="Recuperacion de contrasena - Gestion finanzas personales",
            message=f"Tu codigo de verificacion es: {token} (valido por 15 minutos). Si no solicitaste este cambio, ignora este correo.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True  # Evita 500 en produccion si SMTP falla; siempre devolvemos JSON
        )
        return Response({"message": "Se ha enviado un codigo al correo."}, status=200)
# -----------------------------------------------------------
# VERIFICACIÃƒÆ’Ã¢â‚¬Å“N DE TOKEN DE RECUPERACIÃƒÆ’Ã¢â‚¬Å“N
# -----------------------------------------------------------
class PasswordResetVerifyView(APIView):
    """
    Verifica que el token enviado al correo sea vÃƒÆ’Ã‚Â¡lido.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)  # Valida email y token
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        token = serializer.validated_data["token"]

        try:
            user = User.objects.get(email=email)  # Busca usuario
            reset_token = PasswordResetToken.objects.filter(user=user, token=token).last()  # Busca ÃƒÆ’Ã‚Âºltimo token
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

        # Comprueba si token sigue siendo vÃƒÆ’Ã‚Â¡lido
        if reset_token and reset_token.is_valid():
            return Response({"valid": True}, status=200)

        return Response({"valid": False}, status=400)


# -----------------------------------------------------------
# CONFIRMAR Y CAMBIAR CONTRASEÃƒÆ’Ã¢â‚¬ËœA
# -----------------------------------------------------------
class PasswordResetConfirmView(APIView):
    """
    Permite establecer nueva contraseÃƒÆ’Ã‚Â±a si el token es vÃƒÆ’Ã‚Â¡lido.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(operation_summary='Confirmar reseteo de contrasena', tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email','token','new_password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='user@mail.com'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, example='12345678'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, example='newPass123')
            }
        ),
        responses={200: openapi.Response('OK', examples={'application/json': {'message': 'Contrasena actualizada y sesiones cerradas.'}})}
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)  # Valida datos recibidos
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(email=email)  # Busca usuario
            reset_token = PasswordResetToken.objects.filter(user=user, token=token).last()
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

        if reset_token and reset_token.is_valid():
            user.set_password(new_password)  # Cambia contraseÃƒÆ’Ã‚Â±a
            user.save()

            # Revoca todos los tokens JWT anteriores para cerrar sesiones activas
            for outstanding_token in OutstandingToken.objects.filter(user=user):
                BlacklistedToken.objects.get_or_create(token=outstanding_token)

            # Elimina token usado
            reset_token.delete()
            return Response({"message": "ContraseÃƒÆ’Ã‚Â±a actualizada y sesiones cerradas."}, status=200)

        return Response({"error": "Token invÃƒÆ’Ã‚Â¡lido o expirado."}, status=400)


# -----------------------------------------------------------
# LOGIN Y REFRESH DE TOKENS JWT
# -----------------------------------------------------------
class LoginView(TokenObtainPairView):
    """
    Genera par de tokens (access y refresh) al iniciar sesiÃƒÆ’Ã‚Â³n.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Login (JWT pair)',
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, example='user@mail.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, example='******'),
            }
        ),
        responses={
            200: openapi.Response(
                description='Tokens',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                ),
                examples={'application/json': {
                    'access': 'eyJhbGciOi...access...',
                    'refresh': 'eyJhbGciOi...refresh...'
                }}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshView(TokenRefreshView):
    """
    Permite refrescar token de acceso usando refresh token.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary='Refrescar access token',
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh'],
            properties={'refresh': openapi.Schema(type=openapi.TYPE_STRING)}
        ),
        responses={
            200: openapi.Response(
                description='Nuevo access',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'access': openapi.Schema(type=openapi.TYPE_STRING)}
                ),
                examples={'application/json': {'access': 'eyJhbGciOi...access...'}}
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# -----------------------------------------------------------
# LOGOUT DE USUARIO
# -----------------------------------------------------------
class LogoutView(APIView):
    """
    Revoca tokens JWT para cerrar sesiÃƒÆ’Ã‚Â³n del usuario.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Logout (revocar tokens)',
        tags=['Auth'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'refresh': openapi.Schema(type=openapi.TYPE_STRING)},
            description='Opcional: si no se envÃƒÆ’Ã‚Â­a refresh, se revocan todos los tokens del usuario.'
        )
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh", None)  # Obtiene token refresh enviado
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Revoca token especÃƒÆ’Ã‚Â­fico
                return Response({"detail": "Logout exitoso (refresh token revocado)."}, status=status.HTTP_205_RESET_CONTENT)
            
            # Si no se envÃƒÆ’Ã‚Â­a refresh, revoca todos los tokens del usuario
            tokens = OutstandingToken.objects.filter(user=request.user)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)
            
            return Response({"detail": "Logout exitoso (todos los tokens revocados)."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------
# VISTA DE INFORMACIÃƒÆ’Ã¢â‚¬Å“N BÃƒÆ’Ã‚ÂSICA DEL USUARIO
# -----------------------------------------------------------
class UserInfoView(APIView):
    """
    Devuelve informaciÃƒÆ’Ã‚Â³n bÃƒÆ’Ã‚Â¡sica del usuario autenticado.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary='Info basica del usuario', tags=['Usuarios'],
                        responses={200: openapi.Response('OK', examples={'application/json': {
                            'username': None,
                            'email': 'user@mail.com',
                            'id': 1,
                            'profile_image': None
                        }})})
    def get(self, request):
        user = request.user  # Obtiene usuario autenticado
        img_url = None
        try:
            if user.profile_image:
                img_url = user.profile_image.url
        except Exception:
            img_url = None
        if img_url and not str(img_url).startswith(("http://", "https://")):
            img_url = request.build_absolute_uri(img_url)

        return Response({
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "profile_image": img_url
        })


def _is_superuser(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(_is_superuser)
@transaction.atomic
def approve_signup_view(request, token: str):
    """
    Endpoint al que llega el botÃƒÆ’Ã‚Â³n 'Aceptar solicitud'.
    Requiere que el usuario estÃƒÆ’Ã‚Â© autenticado y sea superusuario.
    """
    if request.method != "GET":
        return HttpResponseBadRequest("MÃƒÆ’Ã‚Â©todo no permitido.")
    try:
        approve_signup_and_send_code(token)
    except Exception as e:
        return HttpResponseBadRequest(f"Error: {e}")
    return HttpResponse("Solicitud aprobada y cÃƒÆ’Ã‚Â³digo enviado al solicitante.")






