from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.core.exceptions import PermissionDenied

from users.models.user import User
from users.models.user_privacity import UserPrivacy
from users.models.socialmedia import SocialMedia
from users.utils.perfil_usuario import acceso_perfil, permiso_editar
from users.forms.perfil_usuario import (
    UserProfileForm, UserProfilePrivacyForm,
    UserProfileSocialMediaForm
)


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """View for the user profile."""
    model = User
    template_name = 'user_profile.html'
    context_object_name = 'user'
    slug_field = 'slug'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        """
        Obtener el usuario a partir del nombre de usuario.
        Obtener el usuario actual.
        """
        username = self.kwargs.get(self.slug_url_kwarg)
        user = get_object_or_404(User, slug=username)
        current_user = self.request.user
        # Función que otorga acceso al perfil de un usuario.
        acceso_perfil.acceso_perfil(user, current_user)
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el usuario objetivo y actual
        user = self.get_object()
        current_user = self.request.user
        user_privacy = get_object_or_404(UserPrivacy, user=user)
        # Pasar los permisos del usuario actual
        context['can_edit'] = permiso_editar.permiso_editar(user, current_user)
        context['user_owner'] = user == current_user
        # Pasar al contexto los formularios
        context['profile_form'] = UserProfileForm(instance=user)
        context['privacy_form'] = UserProfilePrivacyForm(instance=user_privacy)
        context['social_form'] = UserProfileSocialMediaForm(user=user)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update profile view."""
    model = User
    form_class = UserProfileForm
    template_name = 'partials/profile_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        """Obtiene el usuario a partir del slug."""
        username = self.kwargs.get(self.slug_url_kwarg)
        user = get_object_or_404(User, slug=username)
        # Verificar permisos de edición
        if not permiso_editar.permiso_editar(user, self.request.user):
            raise PermissionDenied
        return user

    def form_valid(self, form):
        messages.success(self.request, '¡Perfil actualizado correctamente!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '¡Hubo un error al actualizar tu perfil!')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'username': self.get_object().slug})
    

class ProfilePrivacyView(LoginRequiredMixin, UpdateView):
    """Update user privacy setting view from profile."""
    model = UserPrivacy
    form_class = UserProfilePrivacyForm
    template_name = 'partials/profile_privacy_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        """Obtiene el usuario a partir del slug."""
        username = self.kwargs.get(self.slug_url_kwarg)
        self.user = get_object_or_404(User, slug=username)
        user_privacy = get_object_or_404(UserPrivacy, user=self.user)
        return user_privacy

    def form_valid(self, form):
        messages.success(self.request, '¡Configuración de privacidad actualizada!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocurrió un error al actualizar la configuración de privacidad.')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('users:profile', kwargs={'username': self.user.slug})
    

class ProfileSocialMediaCreateView(LoginRequiredMixin, CreateView):
    """Create social media link for user."""
    model = SocialMedia
    form_class = UserProfileSocialMediaForm
    template_name = 'partials/profile_social_media_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get(self.slug_url_kwarg)
        self.user = get_object_or_404(User, slug=username)
        if (self.user != request.user):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.user
        messages.success(self.request, '¡Red social añadida correctamente!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, '¡Error al añadir la red social!')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('users:profile', kwargs={'username': self.user.slug})


class ProfileSocialMediaDeleteView(LoginRequiredMixin, View):
    """Delete social media link for user."""
    
    def post(self, request, *args, **kwargs):
        social_media_id = self.kwargs.get('pk')
        self.user = request.user
        social_media = get_object_or_404(SocialMedia, id=social_media_id)
        social_media.delete()
        messages.success(request, '¡Red social eliminada correctamente!')
        return redirect('users:profile', username=request.user.slug)
