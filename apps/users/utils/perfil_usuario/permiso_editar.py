def permiso_editar(user, current_user):
    """
    Función que otorga el permiso de editar un perfil de usuario.
    """

    # Obtener el usuario objetivo y actual
    rol_objetivo = user.rol  # Usuario perfil
    rol_actual = current_user.rol  # Usuario actual

    # Administrar permisos
    can_edit = False
    if rol_objetivo.id == 1 or rol_objetivo.id == 2:
        """"""
        if user.id == current_user.id or rol_actual.id == 3 or current_user.is_staff:
            can_edit = True
    elif rol_objetivo.id == 3:
        if user.id == current_user.id or current_user.is_staff:
            can_edit = True
    return can_edit