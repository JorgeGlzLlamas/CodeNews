from django import forms

from users.models.user import User
from users.models.user_privacity import UserPrivacy
from users.models.socialmedia import SocialMedia


class UserProfileForm(forms.ModelForm):
    """Formulario para editar el perfil de un usuario"""

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name',
            'phone', 'bio', 'avatar_image', 'username'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'readonly': True,
                'class': 'form-control',
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+ 52 000 000 0000'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            })
        }


class UserProfilePrivacyForm(forms.ModelForm):
    """
    Formulario para editar la configuración de privacidad
    de los datos de un usuario.
    """

    class Meta:
        model = UserPrivacy
        fields = [
            'username_or_name', 'bio_is_public',
            'email_is_public', 'phone_is_public',
        ]
        widgets = {
            'username_or_name': forms.Select(attrs={
                'class': 'form-select'
            }),
            'bio_is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'email_is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'phone_is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }


class UserProfileSocialMediaForm(forms.ModelForm):
    """
    Formulario para gestionar las redes sociales del usuario.
    Filtra las plataformas para excluir las que el usuario ya ha añadido.
    """

    def __init__(self, *args, **kwargs):
        """Recibir el usuario desde la vista"""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        """Asegurarnos de que tenemos un usuario"""
        if not self.user:
            return

        """Filtrar las opciones del campo 'platform'"""
        existing_platforms_qs = SocialMedia.objects.filter(user=self.user)
        if self.instance and self.instance.pk:
            existing_platforms_qs = existing_platforms_qs.exclude(pk=self.instance.pk)        
        existing_platforms = list(existing_platforms_qs.values_list('platform', flat=True))
        all_choices = SocialMedia.PlaformChoices.choices
        
        # Creamos una nueva lista de opciones, incluyendo solo aquellas
        # cuyo valor NO ESTÁ en la lista de plataformas existentes.
        available_choices = [
            (value, label) for value, label in all_choices if value not in existing_platforms
        ]
        self.fields['platform'].choices = available_choices

    class Meta:
        model = SocialMedia
        fields = [
            'platform', 'link'
        ]
        widgets = {
            'platform': forms.Select(attrs={
                'class': 'form-select'
            }),
            'link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            })
        }
