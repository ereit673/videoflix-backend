from django.conf import settings
from django.core.mail import EmailMultiAlternatives
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
    html_content = f"""
              <html>
                <body>
                  <p>Dear <span style="color:#2563eb">{instance.username}</span>,</p>
                  <br>
                  <p>Thank you for registering with <span style="color:#2563eb">Videoflix</span>. To complete your registration, please click the button below:</p>
                  <a href="{activation_link}"
                     style="display:inline-block;padding:12px 28px;font-size:16px;color:#fff;background-color:#2563eb;text-decoration:none;border-radius:6px;font-weight:bold;margin:24px 0;">
                    Activate Account
                  </a>
                  <p>If you did not create this account, please disregard this email.</p>
                  <br>
                  <p>Best regards,</p>
                  <p><span style="color:#2563eb">Your Videoflix Team</span></p>
                </body>
              </html>
          """

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
    html_content = f"""
        <html>
            <body>
                <p>Hello,</p>
                <br>
                <p>We recently received a request to reset your password. If you made this request, please click on the following link to reset your password:</p>
                <a href="{reset_link}"
                     style="display:inline-block;padding:12px 28px;font-size:16px;color:#fff;background-color:#2563eb;text-decoration:none;border-radius:6px;font-weight:bold;margin:24px 0;">
                    Reset password
                </a>
                <p>Please note that for security reasons, thin link is only valid for 24 hours.</p>
                <p>If you did not request a password reset, please ignore this email.</p>
                <br>
                <p>Best regards,</p>
                <p>Your Videoflix team!</p>
            </body>
        </html>
    """

    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=False)
