from django.urls import path
from django.contrib.auth.views import LogoutView

from users.views import users

app_name = 'users'

urlpatterns = [
    path('registro/',
         users.RegistrationView.as_view(),
         name='register'),
    path('inicio-sesion/',
         users.AuthenticationView.as_view(),
         name='login'),
    path('cerrar-sesion/',
         LogoutView.as_view(next_page='core:home'),
         name='logout')
]
