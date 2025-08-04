from django import forms
from django.contrib.auth.forms import SetPasswordForm


# Formulario para solicitar el restablecimiento de contraseña
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico",
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))


# Formulario para verificar el código
class VerifyCodeForm(forms.Form):
    code = forms.CharField(label="Código de Verificación", max_length=6,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))


class CustomSetPasswordForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Personalizar etiquetas
        self.fields['new_password1'].label = "Nueva contraseña"
        self.fields['new_password2'].label = "Confirma nueva contraseña"

        for name, field in self.fields.items():
            classes = field.widget.attrs.get('class', '').strip()
            base_classes = 'form-control'
            if classes:
                base_classes += f' {classes}'

            # Añadir is-invalid si hay errores
            if self.errors.get(name):
                base_classes += ' is-invalid'

            field.widget.attrs.update({
                'class': base_classes,
                'placeholder': field.label,
                'autocomplete': 'new-password',
            })