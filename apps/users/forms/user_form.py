from django.contrib.auth.forms import UserCreationForm

from users.models.user import User


class UserRegistrationForm(UserCreationForm):
    """Custom form for user registration."""

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2'
        ]
