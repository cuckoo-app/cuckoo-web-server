# from django.conf import settings
from django.contrib.auth import get_user_model
# from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer


class RegistrationSerializer(RegisterSerializer):
    """A user serializer to aid in authentication and authorization."""

    class Meta:
        """Map this serializer to the default django user model."""
        model = get_user_model()
        fields = ('id', 'username', 'email',)
