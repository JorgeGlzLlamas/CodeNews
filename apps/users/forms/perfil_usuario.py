from users.models.user import User
from django import forms


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name',
            'phone', 'bio', 'avatar_image'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4
            })
        }
