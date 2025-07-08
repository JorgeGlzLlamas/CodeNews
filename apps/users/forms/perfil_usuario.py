from django import forms

from users.models.user import User
from users.models.user_privacity import UserPrivacy


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
                'readonly': True
            }),
            'bio': forms.Textarea(attrs={
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
            'email_is_public','phone_is_public',   
        ]
