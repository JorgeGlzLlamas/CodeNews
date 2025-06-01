from django.db import models
from users.models.user import User


class Audit(models.Model):
    """Audit model to track changes in the system."""

    class Actions(models.TextChoices):
        CREATE = 'create', 'Create'
        UPDATE = 'update', 'Update',
        DELETE = 'delete', 'Delete'

    model = models.CharField(
        max_length=50,
        verbose_name='Nombre del modelo',
    )

    object_id = models.PositiveIntegerField(
        verbose_name='ID del objeto'
    )

    action = models.CharField(
        max_length=10,
        choices=Actions.choices,
        verbose_name='Acción realizada'
    )

    description = models.TextField(
        verbose_name='Descripción de la acción',
        blank=True,
        null=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='objetos_creados',
        verbose_name='Usuario que creó el objeto'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='objetos_actualizados',
        verbose_name='Usuario que actualizó el objeto',
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Fecha de actualización',
        null=True,
        blank=True
    )

    audit_version = models.PositiveIntegerField(
        default=1,
        verbose_name='Versión de auditoría'
    )

    class Meta:
        """Meta options for the Audit model."""

        verbose_name = 'Auditoría'
        verbose_name_plural = 'Auditorías'
        ordering = ['model', '-created_at', '-updated_at']

    def __str__(self):
        """String representation of the Audit model."""
        return f"{self.model} - {self.object_id} - {self.action}"
