import random
from django.db import models
from django.conf import settings
from django.utils import timezone
from users.models.user import User


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        # El código expira después de 5 minutos
        return (timezone.now() - self.created_at).seconds > 300

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))