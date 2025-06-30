from django.urls import path
from django.contrib.auth.views import LogoutView, PasswordChangeView
from users.views import users

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('registro/',
         users.RegistrationView.as_view(),
         name='register'),
    path('inicio-sesion/',
         users.AuthenticationView.as_view(),
         name='login'),
    path('cerrar-sesion/',
         LogoutView.as_view(next_page='core:home'),
         name='logout'),
    
    # Profile URLs
    path('perfil/',
         users.ProfileView.as_view(),
         name='profile'),
    path('perfil/actualizar/',
         users.ProfileUpdateView.as_view(),
         name='update_profile'),
    path('perfil/avatar/actualizar/',
         users.AvatarUpdateView.as_view(),
         name='update_avatar'),
    path('perfil/avatar/eliminar/',
         users.AvatarUpdateView.as_view(),
         name='delete_avatar'),
]
    path('cambiar-contrasena/',
         users.CustomPasswordChangeView.as_view(),
         name='change_password')
]
