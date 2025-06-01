from django.db import models
from users.models.user import User
from articles.models.articles import Articles


class ArticlesLikes(models.Model):
    """Model to represent likes on articles."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liked_articles',
        verbose_name='Usuario que dio like'
    )

    article = models.ForeignKey(
        Articles,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Artículo al que se le dio like'
    )

    class Meta:
        verbose_name = 'Like de Artículo'
        verbose_name_plural = 'Likes de Artículos'
        db_table = 'articles_likes'
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} likes {self.article.title}"


class ArticlesFavorites(models.Model):
    """Model to represent users' favorite articles."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_articles',
        verbose_name='Usuario que marcó como favorito'
    )

    article = models.ForeignKey(
        Articles,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Artículo marcado como favorito'
    )

    class Meta:
        verbose_name = 'Artículo Favorito'
        verbose_name_plural = 'Artículos Favoritos'
        db_table = 'articles_favorites'
        unique_together = ('user', 'article')

    def __str__(self):
        return f"{self.user.username} favorited {self.article.title}"
