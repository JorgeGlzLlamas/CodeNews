from users.models.user import User
from users.models.user_privacity import UserPrivacy
from django import forms


class UserProfileForm(forms.ModelForm):
    """Formulario para editar el perfil de un usuario incluyendo ajustes de privacidad."""

    #Campos de privacidad - solo visibles para auatores
    emais_is_public = forms.BooleanField(
        required=False,
        label='¿Quieres que tu correo sea visible por otros usuarios?'
    )
    phone_is_public = forms.BooleanField(
        required=False,
        label='¿Quieres que tu teléfono sea visible por otros usuarios?'
    )
    bio_is_public = forms.BooleanField(
        required=False,
        label='¿Quieres que tu biografía sea visible por otros usuarios?'
    )
    username_or_name = forms.ChoiceField(
        choices=UserPrivacy.NamePrivacy.choices,
        required=False,
        label='Mostrar en perfil:'
    )

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

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Si el usuario es autor, cargamos sus configuraciones de privacidad
        if self.user and hasattr(self.user, 'rol') and self.user.rol.rol.lower() == 'autor':
            try:
                privacy = self.user.privacy
                self.fields['email_is_public'].initial = privacy.email_is_public
                self.fields['phone_is_public'].initial = privacy.phone_is_public
                self.fields['bio_is_public'].initial = privacy.bio_is_public
                self.fields['username_or_name'].initial = privacy.username_or_name
            except UserPrivacy.DoesNotExist:
                pass
        else:
            # Ocultamos los campos de privacidad si no es autor
            for field in ['email_is_public', 'phone_is_public', 'bio_is_public', 'username_or_name']:
                self.fields.pop(field, None)

    def save(self, commit=True):
        user = super().save(commit=False)
        
        if commit:
            user.save()
            
            # Guardamos las configuraciones de privacidad solo para autores
            if hasattr(user, 'rol') and user.rol.rol.lower() == 'autor':
                privacy, created = UserPrivacy.objects.get_or_create(user=user)
                privacy.email_is_public = self.cleaned_data.get('email_is_public', False)
                privacy.phone_is_public = self.cleaned_data.get('phone_is_public', False)
                privacy.bio_is_public = self.cleaned_data.get('bio_is_public', True)
                privacy.username_or_name = self.cleaned_data.get('username_or_name', UserPrivacy.NamePrivacy.USERNAME)
                privacy.save()
        
        return user