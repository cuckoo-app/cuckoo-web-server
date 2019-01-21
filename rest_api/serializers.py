# from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    """Serializer to map the model instance into json format."""

    owner = serializers.ReadOnlyField(source='owner.username')
    # command = serializers.ReadOnlyField(source='mycommand')

    class Meta:
        """Map this serializer to a model and their fields."""
        model = Job
        fields = ('id',
                  'owner',
                  'command',
                  'status',
                  'date_created',
                  'date_modified',
                  'runtime')
        read_only_fields = ('date_created',)


class UserSerializer(serializers.ModelSerializer):
    """A user serializer to aid in authentication and authorization."""

    jobs = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Job.objects.all())

    class Meta:
        """Map this serializer to the default django user model."""
        model = get_user_model()
        fields = ('id', 'username', 'email', 'jobs')
