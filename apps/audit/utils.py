from django.utils import timezone
from core.middleware import get_current_user

from audit.models.audit import Audit

IGNORED = ['Audit']


def _make_description(instance, action, user=None):
    """
    Crea una descripción a partir de la instancia
    y la acción realizada.
    """

    label = f"{instance._meta.model_name}"
    username = user.username if user else "Sistema"
    description = (
        f"{username} {action.capitalize()} en "
        f"{label.capitalize()} con ID {instance.pk}"
    )
    return description


def _get_last_audit(instance):
    """Obtiene la última auditoría para un objeto dado"""

    return Audit.objects.filter(
        object_id=instance.pk,
        model=instance._meta.model_name
    ).order_by('-audit_version').first()


def _create_audit_entry(instance, action):
    """Crea una entrada de auditoría para un objeto dado."""

    label = instance._meta.model_name
    if label in IGNORED:
        return

    user = get_current_user()
    now = timezone.now()

    if action == 'create':
        Audit.objects.create(
            model=label,
            object_id=instance.pk,
            action=Audit.Actions.CREATE,
            description=_make_description(instance, action, user),
            created_by=user,
            created_at=now,
            audit_version=1
        )
    else:
        last_audit = _get_last_audit(instance)
        if not last_audit:
            return

        Audit.objects.create(
            model=label,
            object_id=last_audit.object_id,
            action=(
                Audit.Actions.UPDATE
                if action == 'update'
                else Audit.Actions.DELETE
            ),
            description=_make_description(instance, action, user),
            created_by=last_audit.created_by,
            created_at=last_audit.created_at,
            updated_by=user,
            updated_at=now,
            audit_version=last_audit.audit_version + 1
        )
