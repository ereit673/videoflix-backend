import django_rq

from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django.contrib.auth import get_user_model
from users_app.api.tasks import send_activation_email, send_password_reset_email


User = get_user_model()
password_reset_requested = Signal()


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Handles the user post save signal.
    """
    if created and not instance.is_active:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(send_activation_email, instance)


@receiver(password_reset_requested)
def password_reset_requested_handler(sender, user, **kwargs):
    """
    Handles the password reset requested signal.
    """
    queue = django_rq.get_queue('default', autocommit=True)
    queue.enqueue(send_password_reset_email, user)
