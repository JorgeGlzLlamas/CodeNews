import os
from django.db import models
from django.utils.text import slugify


def image_upload_to(instance, filename):
    """Return custom upload path for user avatars."""
    extension = os.path.splitext(filename)[1]
    category = instance.name if instance.pk else "new_category"
    filename = f"{category}_category{extension}"
    return f"articles/categories/{filename}"


class ArticlesCategory(models.Model):
    """Category model to represent article categories."""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Category Name"
    )

    image = models.ImageField(
        verbose_name="Category Image",
        upload_to=image_upload_to,
        default='vexon/img/logo/category_default.webp'
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
        
        # Validate if the category has an existing image
        try:
            old_image = ArticlesCategory.objects.get(pk=self.pk).image
            # Delete old image if it exists and a new one is provided
            if old_image and self.image and old_image != self.image:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)
        except ArticlesCategory.DoesNotExist:
            pass

        self.full_clean()
        super().save(*args, **kwargs)
