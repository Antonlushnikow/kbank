from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class KbankUser(AbstractUser):
    info = models.TextField(max_length=128, blank=True, verbose_name="о себе")
    is_deleted = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to='users_avatar/',
        blank=True,
        default='/users_avatar/default.png'

    )
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=(now() + timedelta(hours=24)))
    is_active = models.BooleanField(default=False)

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires
