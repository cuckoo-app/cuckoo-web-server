# from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class Job(models.Model):
    """This class represents the Job model."""
    RUNNING = 'RU'
    SUCCESS = 'SU'
    ERROR = 'ER'
    CRASH = 'CR'
    STATUS_CHOICES = (
        (RUNNING, 'Running'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
        (CRASH, 'Crash'),
    )

    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=RUNNING,
    )
    command = models.CharField(max_length=255,
                               blank=False,
                               unique=False, editable=True)
    owner = models.ForeignKey(
        get_user_model(),
        related_name='jobs',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Human readable representation of the model."""
        return "{}".format(self.command)



# LIKEY MOVE THIS SOMEWHERE THAT MAKES MORE SENSE; PREVENT IMPORT ARTIFACTS
# This receiver handles token creation when a new user is created.
@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
