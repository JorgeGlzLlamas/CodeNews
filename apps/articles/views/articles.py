from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

import markdown
import logging
from django.http import HttpResponse, JsonResponse


from articles.models.articles import Articles
from users.models.user_rol import Rol
from articles.forms.article_data import ArticleDataCreateForm, ArticleDataUpdateForm
from articles.forms.article_content import ArticleContentForm


logger = logging.getLogger(__name__)

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


class ArticleContentView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Vista para editar el contenido de un artículo."""
    model = Articles
    form_class = ArticleContentForm
    template_name = 'articles/content_form.html'
    permission_required = 'articles.change_article'
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

    def get_form_kwargs(self):
        """Pasa argumentos adicionales al formulario."""
        kwargs = super().get_form_kwargs()
        if self.request.session.pop('came_from_update', False):
            kwargs['from_update'] = True
        return kwargs
    
    def get_success_url(self):
        return reverse('articles:article_content', kwargs={'title': self.object.slug})

    def post(self, request, *args, **kwargs):
        """Maneja solicitudes POST para vista previa o guardado."""
        if 'preview' in request.POST:
            markdown_content = request.POST.get('content', '')
            html_content = self.process_markdown(markdown_content)
            return HttpResponse(html_content)
        else:
            return super().post(request, *args, **kwargs)

    def process_markdown(self, markdown_content):
        """Procesa el contenido Markdown y devuelve HTML."""
        extensions = [
            'markdown.extensions.fenced_code',    # Bloques de código
            'markdown.extensions.tables',         # Tablas
            'markdown.extensions.nl2br',          # Saltos de línea
            'markdown.extensions.toc',            # Tabla de contenidos
            'markdown.extensions.codehilite',     # Resaltado de sintaxis
            'markdown.extensions.extra',          # Extensiones adicionales
            'markdown.extensions.footnotes',      # Notas al pie
            'markdown.extensions.admonition',     # Cajas de advertencia
        ]

        extension_configs = {
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
                'linenums': False,
            },
            'markdown.extensions.toc': {
                'permalink': True,
                'permalink_class': 'headerlink',
                'permalink_title': 'Enlace permanente a este encabezado',
            }
        }

        md = markdown.Markdown(
            extensions=extensions,
            extension_configs=extension_configs,
            tab_length=4
        )

        html_content = md.convert(markdown_content)

        if not markdown_content.strip():
            html_content = '''
            <div class="text-center text-muted py-5">
                <i class="bi bi-eye display-4 mb-3"></i>
                <h4>Preview aparecerá aquí</h4>
                <p>Comienza a escribir en la pestaña "Escribir" para ver el resultado</p>
            </div>
            '''

        return html_content

    def form_valid(self, form):
        """Maneja el caso de formulario válido."""
        messages.success(self.request, 'Contenido del artículo actualizado.')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Maneja el caso de formulario inválido."""
        messages.error(self.request, 'Ocurrió un error!')
        return super().form_invalid(form)