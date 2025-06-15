from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
import os

from django.contrib.auth.models import AbstractUser
from users.models.user_rol import Rol


def avatar_upload_to(instance, filename):
    """Return custom upload path for user avatars."""
    extension = os.path.splitext(filename)[1]
    username = instance.username if instance.pk else "nuevo_usuario"
    filename = f"{username}_avatar{extension}"
    return f"usuarios/avatars/{filename}"


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    This allows for additional fields and methods in the future.
    """

    email = models.EmailField(
        unique=True
    )

    first_name = models.CharField(
        max_length=100,
        blank=False
    )

    last_name = models.CharField(
        max_length=100,
        blank=False
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

    avatar_image = models.ImageField(
        verbose_name="Avatar",
        upload_to=avatar_upload_to,
        default="usuarios/avatars/default.png",
        blank=True,
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        verbose_name="Rol",
        blank=True,
        null=True
    )

    class Meta:
        """Meta options for the User model."""

        app_label = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = "user"
        unique_together = ('username', 'email')

    def __str__(self):
        return self.username

    def get_full_name(self):
        name = f"{self.first_name} {self.last_name}"
        return name.strip()

    def get_short_name(self):
        return self.first_name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)

    def _validate_avatar_extension(self):
        """
        Validate the file extension of the avatar image.

        Raise ValidationError if the extension is not allowed.
        """
        if not self.avatar_image:
            return

        allowed_extensions = ['.jpg', '.jpeg', '.png', '.webp']
        extension = os.path.splitext(self.avatar_image.name)[1].lower()

        if extension not in allowed_extensions:
            raise ValidationError({
                'avatar_image': (
                    f"La extensión {extension} no es permitida."
                    f"Solo se permiten: {', '.join(allowed_extensions)}."
                )
            })

    def clean(self):
        super().clean()
        self._validate_avatar_extension()
