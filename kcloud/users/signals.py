from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from djoser.signals import user_registered
from .models import User


@receiver(user_registered)
def send_activation_code(sender, user, request, **kwargs):
    user.generate_activation_code()
    subject = "Your activation code"
    message = f"Your activation code is {user.activation_code}. The code is valid for 10 minutes."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])