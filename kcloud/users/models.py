from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from .managers import CustomUserManager
import uuid
from django.utils import timezone


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=True)
    subscription_plan = models.CharField(
        max_length=20,
        choices=[('free', 'Free'), ('basic', 'Basic'), ('premium', 'Premium')],
        default='free'
    )

    storage_limit = models.BigIntegerField(default=5*1024*1024*1024)
    storage_used = models.BigIntegerField(default=0)

    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    last_ip_user = models.GenericIPAddressField(null=True, blank=True)

    two_factor_auth_enabled = models.BooleanField(default=False)
    security_question = models.CharField(max_length=255, null=True, blank=True)
    security_answer_hash = models.CharField(max_length=255, null=True, blank=True)  # Хеш ответа для безопасности

    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    activation_code = models.CharField(max_length=6, blank=True, null=True)
    activation_code_expires = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email}"

    def update_limit(self, file_size):
        self.storage_used += file_size

        if self.storage_used > self.storage_limit:
            raise ValueError('Превышен лимит хранения')

        self.save()

    def generate_activation_code(self):
        self.activation_code = str(uuid.uuid4().int)[:6]
        self.activation_code_expires = timezone.now() + timezone.timedelta(minutes=10)
        self.save()