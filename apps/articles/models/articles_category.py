from django.db import models
from django.utils.text import slugify


class ArticlesCategory(models.Model):
    """Category model to represent article categories."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Category Name"
    )

    slug = models.SlugField(
        max_length=100,
        verbose_name="Category Slug",
        blank=True
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        db_table = 'articles_category'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save method to auto-generate slug from name."""
        self.name = self.name.strip()
        if not self.slug:
            self.slug = slugify(self.name)

        self.full_clean()
        super().save(*args, **kwargs)
