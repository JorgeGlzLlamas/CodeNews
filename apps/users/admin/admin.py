from django.contrib import admin

from users.models.user import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        'username', 'email', 'name', 'slug',
        'paternal_surname', 'maternal_surname',
        'is_active', 'is_staff'
    )
    fieldsets = (
        ('Credenciales', {
            'fields': ('username', 'slug', 'password')
        }),
        ('Información personal', {
            'fields': (
                'name', 'paternal_surname', 'maternal_surname',
                'email', 'phone', 'bio', 'avatar_image'
            )
        }),
        ('Permisos', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Fechas importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    prepopulated_fields = {'slug': ('username',)}
