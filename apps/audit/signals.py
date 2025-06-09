from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from audit.utils import (_create_audit_entry)

IGNORED = ['Audit']


@receiver(post_save)
def audit_save(sender, instance, created, **kwargs):
    """Señal que se ejecuta después de guardar un objeto."""

    action = 'create' if created else 'update'
    _create_audit_entry(instance, action)


@receiver(post_delete)
def audit_delete(sender, instance, **kwargs):
    """Señal que se ejecuta después de eliminar un objeto."""

    _create_audit_entry(instance, 'delete')
