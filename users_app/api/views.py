from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from users_app.api import serializers

User = get_user_model()


class RegistrationView(APIView):
    """
    Handles user registration.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Checks if the user is already registered and creates a new account if not.
        """
        serializer = serializers.RegistrationSerializer(data=request.data)

        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            data = {
                "user": {
                    "id": saved_account.pk,
                    "email": saved_account.email
                },
                "token": "activation_token"
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        response = Response({"message": "Login successful"})

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
        user = User.objects.get(email=request.data['email'])
        response.data = {
            "detail": "Login successful",
            "user": {
                "id": user.pk,
                "username": user.username
            }
        }

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
                "detail": "Refresh token not found"
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except:
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
