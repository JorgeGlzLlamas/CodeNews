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
    
    def is_liked_by(self, user):
        """
        Checks if the comment has been liked by a specific user.
        Returns True if liked, False otherwise.
        """
        # Asegurarnos de que el usuario no sea anónimo para evitar errores
        if user.is_anonymous:
            return False
        # Esta consulta es súper eficiente. .exists() devuelve True/False
        # y no trae el objeto de la base de datos.
        return self.likes_comentarios.filter(user=user).exists()
