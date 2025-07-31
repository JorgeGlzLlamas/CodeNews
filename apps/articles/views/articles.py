from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

from articles.models.articles import Articles
from users.models.user_rol import Rol
from articles.forms.article_data import ArticleDataCreateForm, ArticleDataUpdateForm
from articles.forms.article_content import ArticleContentForm


def set_from_update_view(request, slug):
    request.session['came_from_update'] = True
    return redirect('articles:article_content', title=slug)    


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """View to create an article."""
    model = Articles
    form_class = ArticleDataCreateForm
    template_name = 'articles/create_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        user = self.request.user
        # Asignar el usuario al artículo
        article = form.save(commit=False)
        article.user = user
        article.save()
        # Cambiar el rol del usuario a autor
        user.rol = Rol.objects.get(pk=2)
        user.save()
        messages.success(self.request, 'Metadatos del artículo establecidos. Ahora puedes agregar el contenido.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al crear el artículo.')
        return super().form_invalid(form)

    # Función para redireccionar al detalle del artículo
    def get_success_url(self):
        return reverse('articles:article_content', kwargs={'title': self.object.slug})


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                        UpdateView):
    """View to update an article."""
    model = Articles
    form_class = ArticleDataUpdateForm
    template_name = 'articles/update_form.html'
    permission_required = 'articles.change_article'
    slug_url_kwarg = 'title'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        """Get the article based on the slug."""
        article_name = self.kwargs.get(self.slug_url_kwarg)
        article = get_object_or_404(Articles, slug=article_name)
        return article

    def dispatch(self, request, *args, **kwargs):
        """Check if the user is the owner of the article."""
        article = self.get_object()
        # Check user permissions
        is_owner = article.user == request.user
        is_staff = request.user.is_staff
        is_moderator = request.user.rol.id == 3
        # Apply validation if user has not permission
        if not (is_owner or is_staff or is_moderator):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Artículo actualizado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al actualizar el artículo.')
        return super().form_invalid(form)

    # Función para redireccionar al detalle del artículo
    def get_success_url(self):
        return reverse('articles:article_update', kwargs={'title': self.object.slug})


class ArticleContentView(LoginRequiredMixin, PermissionRequiredMixin,
                                UpdateView):
    """View to create the article content."""
    model = Articles
    form_class = ArticleContentForm
    template_name = 'articles/content_form.html'
    permission_required = 'articles.change_article'
    slug_url_kwarg = 'title'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        """Get the article based on the slug."""
        article_name = self.kwargs.get(self.slug_url_kwarg)
        article = get_object_or_404(Articles, slug=article_name)
        return article

    def dispatch(self, request, *args, **kwargs):
        """Check if the user is the owner of the article."""
        article = self.get_object()
        # Check user permissions
        is_owner = article.user == request.user
        is_staff = request.user.is_staff
        is_moderator = request.user.rol.id == 3
        # Apply validation if user has not permission
        if not (is_owner or is_staff or is_moderator):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Verifica y limpia la sesión
        if self.request.session.pop('came_from_update', False):
            kwargs['from_update'] = True
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Contenido del artículo actualizado.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ocurrió un error!')
        return super().form_invalid(form)
