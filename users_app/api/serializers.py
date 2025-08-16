from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users_app.api.signals import password_reset_requested

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    confirmed_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'password',
            'confirmed_password',
        ]
        extra_kwargs = {
            'email': {'write_only': True,
                      'required': True},
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        """
        Validates the registration data.
        Checks for unallowed fields.
        Checks for password confirmation.
        Checks for existing email.
        """
        allowed_fields = {"email", "password", "confirmed_password"}
        sent_fields = set(self.initial_data.keys())
        extra_fields = sent_fields - allowed_fields
        if extra_fields:
            raise serializers.ValidationError({
                field: "This field is not allowed." for field in extra_fields
            })

        if attrs['password'] != attrs['confirmed_password']:
            raise serializers.ValidationError("Passwords don't match")

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already in use")

        return super().validate(attrs)

    def create(self, validated_data):
        """
        Creates a new inactive user account.
        """
        validated_data.pop('confirmed_password')
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            is_active=False
        )
        user.set_password(validated_data['password'])
        user.save()
        print('USER CREATED NOW', user.is_active)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        """
        Removes the username field from the serializer.
        """
        super().__init__(*args, **kwargs)

        if "username" in self.fields:
            self.fields.pop("username")

    def validate(self, attrs):
        """
        Validates the login credentials.
        Checks for existing user.
        Checks for correct password.
        """
        email = attrs['email']
        password = attrs['password']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        if not user.check_password(password):
            raise serializers.ValidationError("Wrong password")

        attrs['username'] = user.username
        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer for password reset.
    """
    email = serializers.EmailField(required=True)

    def save(self, **kwargs):
        try:
            user = User.objects.get(email=self.validated_data['email'])
            password_reset_requested.send(sender=self.__class__, user=user)
        except User.DoesNotExist:
            pass


class PasswordConfirmationSerializer(serializers.Serializer):
    """
    Serializer for password confirmation
    """
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs

    def create(self, validated_data):
        user = self.context.get('user')
        if user is None:
            raise serializers.ValidationError("User context is required.")
        user.set_password(validated_data['new_password'])
        user.save()
        return user
