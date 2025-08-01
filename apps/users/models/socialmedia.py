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
        YOUTUBE = "youtube", "YouTube"
        OTHER = "other", "Otro"

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

    def get_tabler_classes(self):
        """
        Devuelve un diccionario con las clases de botón e icono de Tabler
        correspondientes a la plataforma.
        """
        # Mapeo de plataformas a clases de Tabler
        class_map = {
            self.PlaformChoices.FACEBOOK:  {'button': 'btn-facebook',  'icon': 'ti-brand-facebook'},
            self.PlaformChoices.GITHUB:    {'button': 'btn-github',    'icon': 'ti-brand-github'},
            self.PlaformChoices.LINKEDIN:  {'button': 'btn-linkedin',  'icon': 'ti-brand-linkedin'},
            self.PlaformChoices.TWITTER:   {'button': 'btn-twitter',   'icon': 'ti-brand-twitter'},
            self.PlaformChoices.INSTAGRAM:{'button': 'btn-instagram', 'icon': 'ti-brand-instagram'},
            self.PlaformChoices.YOUTUBE:   {'button': 'btn-youtube',   'icon': 'ti-brand-youtube'},
            # Valor por defecto para "Otro" o cualquier plataforma no mapeada
            self.PlaformChoices.OTHER:     {'button': 'btn-secondary', 'icon': 'ti-world'},
        }
        # Devuelve la entrada del mapa o un valor por defecto si no se encuentra
        return class_map.get(self.platform, {'button': 'btn-secondary', 'icon': 'ti-link'})

    class Meta:
        """Meta options for the SocialMedia model."""

        app_label = "users"
        verbose_name = "Red Social"
        verbose_name_plural = "Redes Sociales"
        db_table = "social_media"
        unique_together = (("user", "platform"))

    def __str__(self):
        return f"{self.user.username} - {self.platform}"
