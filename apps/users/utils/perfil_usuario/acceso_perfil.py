def acceso_perfil(user, current_user):
    """
    Función que otorga acceso al perfil de un usuario,
    en base al rol de usuario autenticado
    """
    from django.core.exceptions import PermissionDenied

    # Obtener los roles de los usuarios
    rol_objetivo = user.rol  # Usuario perfil
    rol_actual = current_user.rol   # Usuario actual

    if rol_objetivo.id == 1:
        """
        Rol de usuario básico.
        Solo el mismo usuario o un moderador puede ver el perfil del usuario.
        """
        if user.id != current_user.id and rol_actual.id != 3 and not current_user.is_staff:
            raise PermissionDenied
    elif rol_objetivo.id == 2:
        # Rol de autor. Perfil visible para todos lo usuarios
        pass
    elif rol_objetivo.id == 3:
        """
        Rol de moderador.
        Solo el mismo usuario o un moderador puede ver el perfil del usuario.
        """
        if user.id != current_user.id and rol_actual.id != 3 and not current_user.is_staff:
            raise PermissionDenied
    else:
        raise PermissionDenied
    return user