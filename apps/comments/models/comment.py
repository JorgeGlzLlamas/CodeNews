from django.db import models
from users.models.user import User
from articles.models.articles import Articles


class Comment(models.Model):
    """Model for comments on articles."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commentarios',
        verbose_name='Usuario'
    )

    article = models.ForeignKey(
        Articles,
        on_delete=models.CASCADE,
        related_name='commentarios',
        verbose_name='Artículo'
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replicas',
        verbose_name='Comentario padre'
    )

    content = models.TextField(
        max_length=500,
        verbose_name='Contenido'
    )

    class Meta:
        """Meta options for the Comment model."""

        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        db_table = 'comments'

    def __str__(self):
        return f'Comentario de {self.user.username} en {self.article.title}'
