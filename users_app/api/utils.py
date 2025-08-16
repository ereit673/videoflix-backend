from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def generate_activation_link(user):
    """
    Generates an activation link for the user.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    activation_link = f"http://127.0.0.1:8000/api/activate/{uidb64}/{token}/"
    return activation_link


def generate_reset_password_link(user):
    """
    Generates a password reset link for the user.
    """
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_link = f"http://127.0.0.1:8000/api/password_confirm/{uidb64}/{token}/"
    return reset_link
