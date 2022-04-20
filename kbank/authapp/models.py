from django.db import models
from django.contrib.auth.models import AbstractUser


class KbankUser(AbstractUser):
    info = models.TextField(max_length=128, blank=True, verbose_name="о себе")
    is_deleted = models.BooleanField(default=False)
    avatar = models.ImageField(
        upload_to='users_avatar/',
        blank=True,
        default='/users_avatar/default.png'
    )
