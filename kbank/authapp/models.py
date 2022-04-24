from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField


class KbankUser(AbstractUser):
    info = models.TextField(max_length=128, blank=True, verbose_name="о себе")
    is_deleted = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    avatar = ResizedImageField(
        size=[300, 300],
        crop=['middle', 'center'],
        upload_to='users_avatar/',
        blank=True,
        default='/users_avatar/default.png',
        verbose_name='аватар',
    )
