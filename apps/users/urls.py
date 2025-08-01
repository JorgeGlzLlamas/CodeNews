from django.urls import path
from django.contrib.auth.views import LogoutView
from apps.users.views import authentication
from users.views import user_profile

app_name = 'users'

urlpatterns = [
    # Authentication URLs
    path('registro/',
         authentication.RegistrationView.as_view(),
         name='register'),
    path('inicio-sesion/',
         authentication.AuthenticationView.as_view(),
         name='login'),
    path('cerrar-sesion/',
         LogoutView.as_view(next_page='core:home'),
         name='logout'),
    path('cambiar-contrasena/',
         authentication.CustomPasswordChangeView.as_view(),
         name='change_password'),

    # Profile URLs
    path('<slug:username>/perfil/',
         user_profile.ProfileDetailView.as_view(),
         name='profile'),
    path('<slug:username>/editar-perfil/',
         user_profile.ProfileUpdateView.as_view(),
         name='profile_update'),
    path('<slug:username>/editar-privacidad/',
         user_profile.ProfilePrivacyView.as_view(),
         name='profile_privacy'),
    path('nueva-red-social/<slug:username>/',
         user_profile.ProfileSocialMediaCreateView.as_view(),
         name='social_media_create'),
    path('eliminar-red-social/<int:pk>/',
         user_profile.ProfileSocialMediaDeleteView.as_view(),
         name='social_media_delete')
]
