from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from users.models.user import User
from users.models.user_rol import Rol
from social_core.pipeline.social_auth import auth_allowed
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from social_core.exceptions import AuthForbidden

def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'google-oauth2':
        # Actualizar o completar datos del usuario
        if not user.first_name:
            user.first_name = response.get('given_name', '')
        if not user.last_name:
            user.last_name = response.get('family_name', '')
        if not user.email:
            user.email = response.get('email', '')
        
        # Asignar rol por defecto (Usuario)
        if not user.rol:
            default_rol = Rol.objects.get_or_create(rol='Usuario')[0]
            user.rol = default_rol
        
        user.save()

def check_email_exists(backend, details, request, *args, **kwargs):
    email = details.get('email')
    if email:
        from users.models.user import User
        if User.objects.filter(email=email).exists():
            # Si el usuario existe, autentícalo automáticamente
            user = User.objects.get(email=email)
            return {
                'is_new': False,
                'user': user
            }
    return None

def redirect_existing_user(backend, user, request, is_new=False, *args, **kwargs):
    if not is_new and user:
        # Usuario existente - autenticar y redirigir
        from django.contrib.auth import login
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, '¡Tu cuenta ya estaba registrada! Has iniciado sesión correctamente.')
        return redirect(reverse('core:home'))

def check_email_exists(backend, details, response, *args, **kwargs):
    """Verifica si el email ya existe en la base de datos"""
    email = details.get('email')
    if email:
        from users.models.user import User
        if User.objects.filter(email=email).exists():
            return  # Permite el login si el email existe
    raise AuthForbidden(backend)  # Bloquea el acceso si el email no existe

def auto_login(strategy, user, *args, **kwargs):
    """Realiza el login automático y maneja sesiones persistentes"""
    from django.utils import timezone
    from datetime import timedelta
    
    # Verifica si la última sesión fue hace más de una semana
    last_login_threshold = timezone.now() - timedelta(weeks=1)
    
    if user.last_login and user.last_login < last_login_threshold:
        # No hacer autologin si ha pasado más de una semana
        return
    
    # Realiza el login automático
    strategy.request.session.set_expiry(604800)  # 1 semana
    strategy.session_set('user_id', user.pk)  
    login(strategy.request, user, backend='django.contrib.auth.backends.ModelBackend')
    
    return {'user': user}