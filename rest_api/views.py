# from django.conf import settings
from django.contrib.auth import get_user_model
# from django.http import HttpResponse, HttpResponseBadRequest
# from django.core.exceptions import FieldError
from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import JobSerializer, UserSerializer
from .models import Job
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class CreateView(generics.ListCreateAPIView):
    """This class handles the GET and POST requests of our rest api."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new job."""
        # mycommand = self.request.GET.dict()['command']
        # serializer.save(owner=self.request.user, mycommand=mycommand)
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """Only return jobs owned by the currently authenticated user."""
        user = self.request.user
        return Job.objects.filter(owner=user)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles GET, PUT, PATCH and DELETE requests."""
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner)

    def perform_update(self, serializer):
        # if 'command' in self.request.POST.keys():
        #     raise FieldError('Command name cannot be changed!')
        serializer.save()

    def get_queryset(self):
        """Only return jobs owned by the currently authenticated user."""
        user = self.request.user
        return Job.objects.filter(owner=user)


# class UserJobView(generics.ListAPIView):
#     """View to list a user's jobs."""
#     queryset = Job.objects.all()
#     serializer_class = JobSerializer
#     permission_classes = (
#         permissions.IsAuthenticated,
#         IsOwner
#     )

    # def get_queryset(self):
    #     """Only return jobs owned by the currently authenticated user."""
    #     user = self.request.user
    #     return Job.objects.filter(owner=user)


class UserView(generics.ListAPIView):
    """View to list the user queryset."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveAPIView):
    """View to retrieve a user instance."""
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class Logout(APIView):
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
