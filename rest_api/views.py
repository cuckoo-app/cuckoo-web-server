# from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import JobSerializer, UserSerializer
from .models import Job


class CreateView(generics.ListCreateAPIView):
    """This class handles the GET and POST requests of our rest api."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new job."""
        serializer.save(owner=self.request.user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles GET, PUT, PATCH and DELETE requests."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)


class UserJobView(generics.ListAPIView):
    """View to list a user's jobs."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner
    )


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
