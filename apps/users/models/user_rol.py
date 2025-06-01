from django.db import models
from django.contrib.auth.models import Group
from users.models.user import User


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


class UserRol(models.Model):
    """Manages the user's roles."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_roles",
        verbose_name="Usuario"
    )

    rol = models.ForeignKey(
        Rol,
        on_delete=models.PROTECT,
        related_name="user_roles",
        verbose_name="Rol"
    )

    class Meta:
        """Meta options for the UserRol model."""

        app_label = "users"
        verbose_name = "Rol de Usuario"
        verbose_name_plural = "Roles de Usuario"
        db_table = "user_rol"
        unique_together = (("user", "rol"))

    def __str__(self):
        return f"{self.user.username} - {self.rol.rol}"
