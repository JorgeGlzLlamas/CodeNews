from django.contrib import admin
from users.models.user_rol import Rol


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('rol', 'group')
