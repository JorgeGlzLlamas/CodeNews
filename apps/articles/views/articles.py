from django.views.generic import CreateView, UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import DetailView
from django.db.models import F

import markdown
from django.http import HttpResponse
from articles.utils.procesar_markdown import process_markdown_util

from articles.models.articles import Articles
from users.models.user_rol import Rol
from articles.forms.article_data import ArticleDataCreateForm, ArticleDataUpdateForm
from articles.forms.article_content import ArticleContentForm
from comments.forms.comments import CommentForm

import logging
import re
logger = logging.getLogger(__name__)


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
        messages.error(self.request, f'Hubo un error al crear el artículo.{form.errors}')
        return super().form_invalid(form)

    # Función para redireccionar al detalle del artículo
    def get_success_url(self):
        return reverse('articles:article_content', kwargs={'title': self.object.slug})


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """View to update an article."""
    model = Articles
    form_class = ArticleDataUpdateForm
    template_name = 'articles/update_form.html'
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


class ArticleContentView(LoginRequiredMixin, UpdateView):
    """Vista para editar el contenido de un artículo."""
    model = Articles
    form_class = ArticleContentForm
    template_name = 'articles/content_form.html'
    slug_url_kwarg = 'title'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        """Obtiene el artículo basado en el slug."""
        article_name = self.kwargs.get(self.slug_url_kwarg)
        article = get_object_or_404(Articles, slug=article_name)
        return article

    def dispatch(self, request, *args, **kwargs):
        """Verifica si el usuario tiene permisos para editar el artículo."""
        article = self.get_object()
        is_owner = article.user == request.user
        is_staff = request.user.is_staff
        is_moderator = request.user.rol.id == 3
        if not (is_owner or is_staff or is_moderator):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Añade el HTML del preview inicial al contexto."""
        context = super().get_context_data(**kwargs)
        # Generamos el preview del contenido existente en la carga inicial
        initial_content = self.get_object().content or ''
        context['initial_preview_html'] = process_markdown_util(initial_content)
        return context
    
    def form_valid(self, form):
        """Maneja el caso de formulario válido."""
        messages.success(self.request, 'Contenido del artículo actualizado.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Maneja el caso de formulario inválido."""
        messages.error(self.request, 'Ocurrió un error!')
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse('articles:article_content', kwargs={'title': self.object.slug})


class MarkdownPreviewView(View):
    """Procesa y devuelve un preview de Markdown."""
    
    def post(self, request, *args, **kwargs):
        markdown_content = request.POST.get('content', '')
        # Aquí puedes añadir la misma lógica de permisos si quieres proteger el endpoint
        # por ejemplo, verificando que el usuario esté autenticado.
        html_content = process_markdown_util(markdown_content)
        return HttpResponse(html_content)


class ArticleDetailView(DetailView):
    model = Articles
    template_name = 'articles/article_detail.html'
    context_object_name = 'article'
    slug_url_kwarg = 'slug'

    def get(self, request, *args, **kwargs):
        """
        Sobrescribimos el método GET para incrementar el contador de vistas.
        """
        self.object = self.get_object()
        Articles.objects.filter(pk=self.object.pk).update(views_count=F('views_count') + 1)
        self.object.refresh_from_db()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
        html = md.convert(self.object.content)

        # Divide en secciones por <h2> o <h3>
        secciones = re.split(r'(?=<h2>|<h3>)', html)
        context['sections'] = secciones  # Lista con cada bloque

        # Comentarios
        comentarios = self.object.commentarios.all().order_by('-id')
        # Artículo
        article = self.object
        if self.request.user.is_authenticated:
            article.is_favorited = article.is_favorited_by(self.request.user)
            for comment in comentarios:
                # Verficamos si el usuario ha dado like al comentario (True/False)
                comment.user_has_liked = comment.is_liked_by(self.request.user)
        context['comentarios'] = comentarios
        context['comment_form'] = CommentForm()
        return context