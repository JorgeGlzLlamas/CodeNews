from django.db import models
from users.models.user import User


class SocialMedia(models.Model):
    """Manages the user's social media accounts."""

    class PlaformChoices(models.TextChoices):
        """Choices for the social media platform."""

        FACEBOOK = "facebook", "Facebook"
        GITHUB = "github", "GitHub"
        LINKEDIN = "linkedin", "LinkedIn"
        TWITTER = "twitter", "Twitter"
        INSTAGRAM = "instagram", "Instagram"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="social_media",
        verbose_name="Usuario"
    )

    platform = models.CharField(
        max_length=30,
        choices=PlaformChoices.choices,
        default=PlaformChoices.FACEBOOK,
        verbose_name="Plataforma",
    )

    link = models.URLField(
        verbose_name="Enlace",
        max_length=200,
    )

    class Meta:
        """Meta options for the SocialMedia model."""

        app_label = "users"
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        db_table = "social_media"
        unique_together = (("user", "platform"))

    def __str__(self):
        return f"{self.user.username} - {self.platform}"
