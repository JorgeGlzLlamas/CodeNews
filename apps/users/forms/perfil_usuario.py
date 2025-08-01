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
            'email_is_public','phone_is_public',   
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
