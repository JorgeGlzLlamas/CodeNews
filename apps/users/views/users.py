from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
import os

from users.forms.user_form import UserRegistrationForm
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


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if 'user_id' in request.session:
            del request.session['user_id']
        messages.success(request, 'Has cerrado sesión correctamente.')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, TemplateView):
    """Profile view for users."""
    template_name = 'perfil_usuario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update profile view."""
    model = User
    fields = ['email', 'first_name', 'last_name', 'phone', 'bio']
    template_name = 'perfil_usuario.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado correctamente')
        return super().form_valid(form)


class AvatarUpdateView(LoginRequiredMixin, UpdateView):
    """Update avatar view."""
    model = User
    fields = ['avatar_image']
    template_name = 'perfil_usuario.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        if 'avatar_image' in self.request.FILES:
            try:
                response = super().form_valid(form)
                messages.success(self.request, 'Avatar actualizado correctamente')
                return response
            except ValidationError as e:
                messages.error(self.request, str(e))
                return redirect(self.success_url)
        return redirect(self.success_url)


class AvatarUpdateView(LoginRequiredMixin, UpdateView):
    """Update avatar view."""
    model = User
    fields = ['avatar_image']
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        new_avatar = request.FILES.get('avatar_image')

        if not new_avatar:
            messages.error(request, 'No se ha seleccionado ningún archivo')
            return redirect(self.success_url)

        # Validar extensión del archivo
        valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        extension = os.path.splitext(new_avatar.name)[1].lower()
        if extension not in valid_extensions:
            messages.error(request, f'Formato no permitido. Use: {", ".join(valid_extensions)}')
            return redirect(self.success_url)

        # Eliminar el avatar anterior si existe y no es el default
        if user.avatar_image and user.avatar_image.name != 'usuarios/avatars/default.png':
            try:
                default_storage.delete(user.avatar_image.path)
            except Exception as e:
                messages.warning(request, f'No se pudo eliminar el avatar anterior: {str(e)}')

        # Guardar el nuevo avatar
        try:
            user.avatar_image = new_avatar
            user.save()
            messages.success(request, 'Avatar actualizado correctamente')
        except Exception as e:
            messages.error(request, f'Error al actualizar el avatar: {str(e)}')

        return redirect(self.success_url)
