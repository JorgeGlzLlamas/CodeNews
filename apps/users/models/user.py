from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    This allows for additional fields and methods in the future.
    """

    first_name = None
    last_name = None

    name = models.CharField(
        max_length=150,
        verbose_name="Nombre",
        blank=True,
    )
    paternal_surname = models.CharField(
        max_length=150,
        verbose_name="Apellido Paterno",
        blank=True,
        null=True,
    )
    maternal_surname = models.CharField(
        max_length=150,
        verbose_name="Apellido Materno",
        blank=True,
        null=True,
    )

    phone = models.CharField(
        max_length=150,
        verbose_name="Teléfono",
        blank=True,
        null=True,
    )

    bio = models.TextField(
        verbose_name="Biografía",
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        verbose_name="Slug",
        unique=True,
        blank=True,
    )

    class Meta:
        """Meta options for the User model."""

        app_label = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"

    def __str__(self):
        return self.username

    def get_full_name(self):
        name = f"{self.name} {self.paternal_surname} {self.maternal_surname}"
        return name.strip()

    def get_short_name(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
