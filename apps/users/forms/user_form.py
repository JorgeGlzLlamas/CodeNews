from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            # No lanzar error, permitiremos el login automático
            self.user_exists = user
        return email

    def save(self, request):
        if hasattr(self, 'user_exists'):
            # Usuario existe - autenticar y redirigir
            user = self.user_exists
            login(request, user)
            raise ValidationError(
                '¡Tu cuenta ya estaba registrada! Has iniciado sesión automáticamente.',
                code='existing_user'
            )
        else:
            # Crear nuevo usuario
            return super().save(commit=True)

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="Recordar mi sesión por 1 semana"
    )