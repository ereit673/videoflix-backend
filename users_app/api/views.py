from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

from users_app.api import serializers

User = get_user_model()


class RegistrationView(APIView):
    """
    Handles user registration.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """Register a new user as inactive."""
        serializer = serializers.RegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response({
            "user": {
                "id": user.pk,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)


class ActivateAccountView(APIView):
    """
    Handles account activation.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request, uidb64, token):
        """
        Activates the user account if the token is valid.
        """
        try:
            user_id = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"detail": "Account successfully activated."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenObtainPairView(TokenObtainPairView):
    """
    Handles token generation for user login.
    """
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Generates a new access and refresh token for the user.
        Sets the tokens as HttpOnly cookies in the response.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]
        user = User.objects.get(email=request.data['email'])
        response = Response({
            "detail": "Login successful",
            "user": {
                "id": user.pk,
                "username": user.username
            }
        })
        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    Handles token refresh for user login.
    """

    def post(self, request, *args, **kwargs):
        """
        Refreshes the access token using the refresh token.
        Sets new access token as HttpOnly cookie in the response.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token is None:
            return Response({
                "detail": "Refresh token not found."
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={"refresh": refresh_token})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({
                "detail": "Refresh token invalid"
            }, status=status.HTTP_401_UNAUTHORIZED)
        access_token = serializer.validated_data.get('access')
        response = Response({
            "detail": "Token refreshed",
            "access": str(access_token)
        })
        response.set_cookie(
            key="access_token",
            value=str(access_token),
            httponly=True,
            secure=True,
            samesite='Lax'
        )
        return response


class CookieTokenBlacklistView(TokenBlacklistView):
    """
    Handles token blacklisting for user logout and deletes all associated tokens from the cookies.
    """

    def post(self, request, *args, **kwargs):
        """
        Blacklists the refresh token for user logout and deletes all associated tokens from the cookies.
        """
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        else:
            return Response({
                "detail": "Refresh token not found."
            }, status=status.HTTP_400_BAD_REQUEST)
        response = Response({
            "detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."
        })
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response


class ResetPasswordView(APIView):
    """
    Handles password reset requests.
    """
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        """
        Initiates the password reset process.
        """
        serializer = serializers.ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "An email has been sent to reset your password."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordConfirmView(APIView):
    """
    Handles password reset confirmation.
    """
    authentication_classes = []

    def post(self, request, uidb64, token, *args, **kwargs):
        """
        Confirms the password reset and sets the new password.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"detail": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.PasswordConfirmationSerializer(
            data=request.data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "detail": "Your Password has been successfully reset."
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
