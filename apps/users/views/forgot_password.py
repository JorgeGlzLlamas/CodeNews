# en tu_app/views.py
from django.views.generic import FormView
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from users.forms.forgot_password import PasswordResetRequestForm, VerifyCodeForm, CustomSetPasswordForm
from users.models.password_reset import PasswordResetCode
from users.models.user import User
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm



class RequestPasswordResetView(FormView):
    template_name = 'accounts/request_password_reset.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('users:verify_code')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            
            # Invalidar códigos anteriores del mismo usuario
            PasswordResetCode.objects.filter(user=user).delete()

            # Crear y guardar el nuevo código
            code = PasswordResetCode.generate_code()
            PasswordResetCode.objects.create(user=user, code=code)

            # Enviar correo electrónico
            mail_subject = 'Código de Verificación para Restablecer Contraseña'
            message = render_to_string('emails/password_reset_code.html', {
                'user': user,
                'code': code
            })
            send_mail(mail_subject, message, None, [email])

            # Guardar el email en la sesión para el siguiente paso
            self.request.session['reset_email'] = email

        except User.DoesNotExist:
            # Para no revelar si un usuario existe o no, no mostramos un error.
            # Simplemente redirigimos como si todo hubiera ido bien.
            pass
            
        return super().form_valid(form)


class VerifyCodeView(FormView):
    template_name = 'accounts/verify_code.html'
    form_class = VerifyCodeForm
    success_url = reverse_lazy('users:reset_new_password')

    def form_valid(self, form):
        email = self.request.session.get('reset_email')
        code = form.cleaned_data['code']
        
        if not email:
            messages.error(self.request, "La sesión ha expirado o es inválida.")
            return redirect('request_password_reset')

        try:
            user = User.objects.get(email=email)
            # Solo se considera el último código generado
            reset_instance = PasswordResetCode.objects.filter(user=user).latest('created_at')

            if reset_instance.code == code and not reset_instance.is_expired():
                # El código es válido. Marcarlo como usado en la sesión.
                self.request.session['is_verified'] = True
                return super().form_valid(form)
            else:
                messages.error(self.request, "El código es incorrecto o ha expirado.")
        except (User.DoesNotExist, PasswordResetCode.DoesNotExist):
            messages.error(self.request, "Error de validación.")
            
        return self.form_invalid(form)


class CustomPasswordResetConfirmView(FormView):
    template_name = 'accounts/reset_new_password.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('users:login')

    def dispatch(self, request, *args, **kwargs):
        """
        Verifica la sesión antes de que cualquier otra cosa ocurra.
        """
        if not request.session.get('is_verified', False):
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return redirect('request_password_reset')

        email = request.session.get('reset_email')
        if not email:
            messages.error(request, "La sesión ha expirado. Por favor, inicia el proceso de nuevo.")
            return redirect('request_password_reset')

        try:
            # Adjuntamos el usuario al objeto de la vista ('self') para poder usarlo después
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "El usuario asociado a esta sesión ya no existe.")
            # Limpiamos la sesión por seguridad
            request.session.flush() 
            return redirect('request_password_reset')

        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Pasa el objeto de usuario al constructor del formulario.
        SetPasswordForm requiere un argumento 'user'.
        """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        """
        El formulario es válido, así que guardamos la nueva contraseña.
        """
        # SetPasswordForm se encarga de cambiar la contraseña y hashearla
        form.save()
        
        # Enviar correo de confirmación
        mail_subject = 'Tu contraseña ha sido restablecida'
        # Suponiendo que tienes una URL con name='home'
        home_url = self.request.build_absolute_uri(reverse_lazy('core:home')) 
        message = render_to_string('emails/password_reset_complete.html', {
            'user': self.user,
            'home_url': home_url
        })
        send_mail(mail_subject, message, None, [self.user.email])
        
        # Limpiar la sesión para que no se pueda reutilizar
        self.request.session.pop('reset_email', None)
        self.request.session.pop('is_verified', None)
        
        messages.success(self.request, "Tu contraseña ha sido cambiada exitosamente.")
        return super().form_valid(form)