from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from users_app.api.utils import generate_activation_link, generate_reset_password_link


def send_activation_email(instance):
    """
    Sends an activation email with a frontend activation link.
    """
    activation_link = generate_activation_link(instance)

    subject = "Confirm your email"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = instance.email
    text_content = f"Please confirm your email using this link: {activation_link}"
    html_content = render_to_string(
        'emails/activation_email.html',
        {'activation_link': activation_link, 'username': instance.username}
    )

    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)


def send_password_reset_email(user):
    """
    Sends an email to the user with a link to reset their password.
    """
    reset_link = generate_reset_password_link(user)
    subject = "Reset your password"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user.email
    text_content = f"Please reset your password using this link: {reset_link}"

    html_content = render_to_string(
        'emails/reset_password_email.html',
        {'reset_link': reset_link}
    )

    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
