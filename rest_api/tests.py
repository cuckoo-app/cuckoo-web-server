from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from .models import Job


# Create your tests here.
class ModelTestCase(TestCase):
    """This class defines the test suite for the Job model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.job_command = "echo 'Hello, world.'"
        self.job = Job(command=self.job_command, owner_id=1)

    def test_model_can_create_a_job(self):
        """Test that the Job model can successfully create a Job."""
        old_count = Job.objects.count()
        self.job.save()
        new_count = Job.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewsTestCase(TestCase):
    """Testing for api views."""

    def setUp(self):
        """Definte the test client and other test variables."""
        user = get_user_model().objects.create(username="my_user")

        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.job_data = {'command': "echo 'Hello, world.'",
                         'owner': user.id,
                         'status': Job.RUNNING}
        self.response = self.client.post(
            reverse('create'),
            self.job_data,
            format="json",
        )

    def test_job_creation(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization(self):
        new_client = APIClient()
        response = new_client.get(reverse('details', kwargs={'pk': 3}),
                                  format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_getting_job(self):
        job = Job.objects.get(pk=1)
        response = self.client.get(
            reverse('details', kwargs={'pk': job.id}),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, job)

    def test_updating_job(self):
        job = Job.objects.get(pk=1)
        change_job = {'status': Job.SUCCESS}
        response = self.client.patch(
            reverse('details', kwargs={'pk': job.id}),
            change_job,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_deleting_jobs(self):
        job = Job.objects.get(pk=1)
        response = self.client.delete(
            reverse('details', kwargs={'pk': job.id}),
            format="json",
            follow=True,
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
