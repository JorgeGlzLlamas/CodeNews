from django.db import models
from users.models.user import User
from articles.models.articles_category import ArticlesCategory
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Articles(models.Model):
    """Article model to represent articles in the system."""

    class ArticleStatus(models.TextChoices):
        """Enumeration for article status."""

        DRAFT = 'draft', 'Borrador'
        PUBLISHED = 'published', 'Publicado'
        ARCHIVED = 'archived', 'Archivado'

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='articles',
        verbose_name='Autor del Artículo'
    )

    category = models.ForeignKey(
        ArticlesCategory,
        on_delete=models.PROTECT,
        related_name='articles',
        verbose_name='Categoría del Artículo'
    )

    title = models.CharField(
        max_length=100,
        verbose_name='Título del Artículo',
        unique=True
    )

    slug = models.SlugField(
        max_length=100,
        verbose_name='Slug del Artículo',
        blank=True,
        unique=True
    )

    content = models.TextField(
        verbose_name='Contenido del Artículo',
        blank=True
    )

    description = models.CharField(
        max_length=200,
        verbose_name='Descripción del Artículo',
        blank=True
    )

    thumbnail_image = models.ImageField(
        upload_to='articles/thumbnails/',
        verbose_name='Imagen en miniatura del Artículo',
        blank=True,
    )

    status = models.CharField(
        max_length=10,
        choices=ArticleStatus.choices,
        default=ArticleStatus.DRAFT,
        verbose_name='Estado del Artículo'
    )

    published_at = models.DateTimeField(
        verbose_name='Fecha de Publicación',
        blank=True,
        null=True
    )

    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Vistas del Artículo'
    )

    shares_count = models.PositiveIntegerField(
        default=0,
        verbose_name='Compartidos del Artículo'
    )

    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        db_table = 'articles'
        ordering = ['-published_at']

    def __str__(self):
        return self.title or self.slug

    def clean(self):
        super().clean()
        self._validate_unique_title()

    def _validate_unique_title(self):
        """Ensure the title is unique."""

        if Articles.objects.exclude(pk=self.pk).filter(
            title__iexact=self.title.strip()
        ).exists():
            raise ValidationError(
                {'title': 'Ya existe un artículo con este título.'}
            )

    def save(self, *args, **kwargs):
        """Override save method to auto-generate slug from title."""
        self.title = self.title.strip()
        if not self.slug:
            self.slug = slugify(self.title)

        self.full_clean()
        super().save(*args, **kwargs)
