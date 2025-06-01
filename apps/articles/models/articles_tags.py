from django.db import models
from articles.models.articles import Articles


class Tags(models.Model):
    """Model for article tags."""

    name = models.CharField(
        max_length=20,
        verbose_name='Nombre de la Etiqueta',
        unique=True
    )

    class Meta:
        verbose_name = 'Etiqueta'
        verbose_name_plural = 'Etiquetas'
        db_table = 'tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)


class ArticlesTags(models.Model):
    """Model to associate articles with tags."""

    article = models.ForeignKey(
        Articles,
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='Artículo'
    )

    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Etiqueta'
    )

    class Meta:
        verbose_name = 'Artículo Etiqueta'
        verbose_name_plural = 'Artículos Etiquetas'
        db_table = 'articles_tags'
        unique_together = ('article', 'tag')

    def __str__(self):
        return f"{self.article.title} - {self.tag.name}"
