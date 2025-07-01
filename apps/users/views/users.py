from django.urls import reverse
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


from users.forms.user_form import UserRegistrationForm
from users.forms.perfil_usuario import UserProfileForm
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
        messages.success(
            self.request,
            '¡Tu cuenta ya estaba registrada!.'
        )
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('users:login')


class AuthenticationView(LoginView):
    """Authentication view for users."""
    authentication_form = AuthenticationForm
    template_name = 'authentication.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Has iniciado sesión correctamente!')
        return response

    def get_success_url(self):
        return reverse('core:home')


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Change password view for users."""
    template_name = 'change_password.html'

    def form_valid(self, form):
        messages.success(
            self.request,
            '¡Tu contraseña ha sido cambiada!'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            '¡Hubo un error al cambiar tu contraseña!'
        )
        return super().form_invalid(form)

    def get_success_url(self):
        # Cambiar la URL de redirección a perfil de usuario
        return reverse('core:home')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update profile view."""

    model = User
    form_class = UserProfileForm
    template_name = 'perfil_usuario.html'

    def form_valid(self, form):
        messages.success(self.request, '¡Perfil actualizado correctamente!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '¡Hubo un error al actualizar tu perfil!')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'pk': self.request.user.pk})
