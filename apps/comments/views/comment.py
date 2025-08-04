from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib import messages
from django.urls import reverse

from comments.models.comment import Comment
from comments.forms.comments import CommentForm
from articles.models.articles import Articles


class CommentView(LoginRequiredMixin, CreateView):
    """View for creating comments on articles."""
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        article_id = kwargs.get('article_id')
        self.article = get_object_or_404(Articles, id=article_id)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.user = self.request.user
        comment.article = self.article
        comment.save()
        messages.success(self.request, 'Tu comentario ha sido publicado.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al publicar tu comentario!')
        return super().form_invalid(form)

    def get_success_url(self):
        # Construimos la URL de redirección.
        base_url = reverse('articles:article_detail', kwargs={'slug': self.article.slug})
        anchor = '#comentarios'
        redirect_url = f"{base_url}{anchor}"

        # Redirigimos al detalle del artículo, anclando en la sección de comentarios.
        return redirect_url
