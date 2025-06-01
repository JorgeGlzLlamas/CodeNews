from django.db import models
from users.models.user import User


class UserPrivacy(models.Model):
    """Manages user privacy settings."""

    class NamePrivacy(models.TextChoices):
        """Choices for the username or name privacy setting."""

        USERNAME = "username", "Nombre de usuario"
        NAME = "name", "Nombre completo"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="privacy",
        verbose_name="Usuario",
    )

    email_is_public = models.BooleanField(
        default=False,
        verbose_name="Email público",
    )

    phone_is_public = models.BooleanField(
        default=False,
        verbose_name="Teléfono público",
    )

    bio_is_public = models.BooleanField(
        default=True,
        verbose_name="Biografía pública",
    )

    username_or_name = models.CharField(
        max_length=8,
        choices=NamePrivacy.choices,
        default=NamePrivacy.USERNAME,
        verbose_name="Nombre público"
    )

    class Meta:
        """Meta options for the UserPrivacy model."""

        app_label = "users"
        verbose_name = "Configuración de Privacidad del Usuario"
        verbose_name_plural = "Configuraciones de Privacidad de Usuarios"
        db_table = "user_privacy"

    def __str__(self):
        return f"Privacidad de {self.user.username}"
