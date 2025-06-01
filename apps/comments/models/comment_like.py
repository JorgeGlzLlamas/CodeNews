from django.db import models
from users.models.user import User
from comments.models.comment import Comment


class CommentLike(models.Model):
    """Model for likes on comments."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes_comentarios',
        verbose_name='Usuario'
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='likes_comentarios',
        verbose_name='Comentario'
    )

    class Meta:
        """Meta options for the CommentLike model."""

        verbose_name = 'Me gusta en comentario'
        verbose_name_plural = 'Me gusta en comentarios'
        db_table = 'comment_likes'
        unique_together = ('user', 'comment')
