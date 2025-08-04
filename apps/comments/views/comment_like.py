from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.contrib import messages
from django.urls import reverse

from comments.models.comment_like import CommentLike
from comments.models.comment import Comment


class CommentLikeToggleView(LoginRequiredMixin, View):
    """
    Handles toggling a like on a comment.
    If the user has already liked the comment, it removes the like.
    Otherwise, it adds a like.
    """

    def post(self, request, comment_id):
        """Handle POST request to toggle a like on a comment."""
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user

        # Usamos get_or_create, que es perfecto para este caso de "toggle"
        # Devuelve el objeto y un booleano 'created' que nos dice si se creó o ya existía.
        like, created = CommentLike.objects.get_or_create(user=user, comment=comment)

        if created:
            # Si el objeto fue creado, significa que el usuario acaba de dar "me gusta".
            messages.success(request, 'Le has dado me gusta al comentario.')
        else:
            # Si 'created' es False, el "me gusta" ya existía. Lo eliminamos.
            like.delete()
            messages.success(request, 'Has quitado tu me gusta al comentario.')

        # Construimos la URL de redirección.
        base_url = reverse('articles:article_detail', kwargs={'slug': comment.article.slug})
        anchor = '#comentarios'
        redirect_url = f"{base_url}{anchor}"

        # Redirigimos al detalle del artículo, anclando en la sección de comentarios.
        return redirect(redirect_url)