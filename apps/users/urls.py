from django.urls import path
from django.contrib.auth.views import LogoutView
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
    path('cambiar-contrasena/',
         users.CustomPasswordChangeView.as_view(),
         name='change_password'),

    # Profile URLs
    path('perfil/<int:pk>/',
         users.ProfileUpdateView.as_view(),
         name='profile'),
]
