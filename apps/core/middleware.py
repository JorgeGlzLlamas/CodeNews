import contextvars
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import login
from django.contrib.auth.models import User

# Creamos el ContextVar con valor por defecto None
_current_user: contextvars.ContextVar = (
    contextvars.ContextVar('current_user', default=None)
)


def get_current_user():
    """
    Devuelve el user almacenado en el contexto actual
    (o None si no hay ninguno).
    """
    return _current_user.get()


class CurrentUserMiddleware:
    """
    Middleware que guarda request.user en un ContextVar,
    compatible con sync y async.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo almacenamos usuarios autenticados
        user = getattr(request, 'user', None)
        if user and getattr(user, 'is_authenticated', False):
            # Set devuelve un token para luego resetear
            token = _current_user.set(user)
        else:
            token = None

        try:
            # Llamamos a la vista (o siguiente middleware)
            response = self.get_response(request)
            return response
        finally:
            # Siempre limpiamos el contexto para evitar "filtraciones"
            if token is not None:
                _current_user.reset(token)

class AutoLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            user_id = request.session.get('user_id')
            if user_id:
                try:
                    user = User.objects.get(pk=user_id)
                    # Verificar que no haya pasado más de una semana
                    last_login_threshold = timezone.now() - timedelta(weeks=1)
                    if user.last_login and user.last_login > last_login_threshold:
                        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                except User.DoesNotExist:
                    pass
        
        response = self.get_response(request)
        return response