from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import AuthenticationForm
from users.forms.user_form import UserRegistrationForm
from django.contrib.auth import authenticate
from django.contrib import messages

from users.models.user import User
from users.models.user_rol import Rol


class RegistrationView(CreateView):
    """Registration view for users."""

    model = User
    form_class = UserRegistrationForm
    template_name = 'registration.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.rol = Rol.objects.get(pk=1)  # Rol 1 = Usuario
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al registrarte.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('users:login')


class AuthenticationView(LoginView):
    """Authentication view for users."""

    authentication_form = AuthenticationForm
    template_name = 'authentication.html'

    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f'¡Bienvenido {user.username} a CodeNews!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:home')
