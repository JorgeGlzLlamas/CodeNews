from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models.user import User


class UserRegistrationForm(UserCreationForm):
    """Custom form for user registration."""

    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md py-2.5 px-4 text-dark text-base font-medium border-gray-300 focus:border-primary focus:outline-0 focus:ring-0 placeholder:text-light',
            'placeholder': 'Contraseña',
            'autocomplete': 'new-password',
        })
    )

    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md py-2.5 px-4 text-dark text-base font-medium border-gray-300 focus:border-primary focus:outline-0 focus:ring-0 placeholder:text-light',
            'placeholder': 'Confirmar contraseña',
            'autocomplete': 'new-password',
        })
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'block w-full rounded-md py-2.5 px-4 text-dark text-base font-medium border-gray-300 focus:border-primary focus:outline-0 focus:ring-0 placeholder:text-light',
                'placeholder': 'Nombre de usuario',
                'autocomplete': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full rounded-md py-2.5 px-4 text-dark text-base font-medium border-gray-300 focus:border-primary focus:outline-0 focus:ring-0 placeholder:text-light',
                'placeholder': 'Correo electrónico',
                'autocomplete': 'email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md py-2.5 px-4 text-dark text-base font-medium border-gray-300 focus:border-primary focus:outline-0 focus:ring-0 placeholder:text-light',
                'placeholder': 'Nombre',
                'autocomplete': 'given-name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'block w-full rounded-md py-2.5 px-4 text-dark text-base font-medium border-gray-300 focus:border-primary focus:outline-0 focus:ring-0 placeholder:text-light',
                'placeholder': 'Apellido',
                'autocomplete': 'family-name'
            }),
        }


class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'block w-full rounded-md py-2.5 px-4 text-dark text-base font-medium border-gray-300 focus:border-primary focus:outline-0 focus:ring-0 placeholder:text-light',            
            'placeholder': 'Nombre de usuario',
            'autocomplete': 'username',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'block w-full rounded-md py-2.5 px-4 text-dark text-base font-medium border-gray-300 focus:border-primary focus:outline-0 focus:ring-0 placeholder:text-light mb-4',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password',
        })
    )