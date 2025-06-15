from django.db import models
from django.contrib.auth.models import Group


class Rol(models.Model):
    """Roles for users."""

    rol = models.CharField(
        max_length=50,
        verbose_name="Rol",
        unique=True,
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.PROTECT,
        verbose_name="Grupo",
        related_name="roles",
        blank=True,
        null=True,
    )

    class Meta:
        """Meta options for the Rol model."""

        app_label = "users"
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        db_table = "rol"

    def __str__(self):
        return self.rol
