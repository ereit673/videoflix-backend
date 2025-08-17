from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom authentication class to authenticate users via JWT stored in cookies.
    """

    def authenticate(self, request):
        """
        Authenticate a user via the JWT stored in the 'access_token' cookie.

        Returns a (user, token) tuple if successful, or None if the cookie is missing.
        Raises AuthenticationFailed if the token is invalid or expired.
        """
        cookie_token = request.COOKIES.get("access_token")
        if not cookie_token:
            return None

        validated_token = self.get_validated_token(cookie_token)
        return self.get_user(validated_token), validated_token
