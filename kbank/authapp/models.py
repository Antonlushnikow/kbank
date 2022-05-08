from datetime import timedelta, datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django_resized import ResizedImageField
from django.utils.timezone import now


def default_key_expires():
    return now() + timedelta(hours=24)


class KbankUser(AbstractUser):
    info = models.TextField(max_length=128, blank=True, verbose_name="о себе")
    is_deleted = models.BooleanField(default=False)
    is_moderator = models.BooleanField(default=False)
    avatar = ResizedImageField(
        size=[300, 300],
        crop=['middle', 'center'],
        upload_to='users_avatar/',
        blank=True,
        default='users_avatar/default.png',
        verbose_name='аватар',
    )
    email = models.EmailField(blank=True, unique=True, verbose_name="Email")
    activation_key = models.CharField(max_length=128, blank=True)
    activation_key_expires = models.DateTimeField(default=default_key_expires)
    is_active = models.BooleanField(default=False)
    block_expires = models.DateTimeField(unique=False, default=datetime(1970, 1, 1))
    moderation_required = models.BooleanField(default=True, verbose_name='Требуется модерация')

    def is_activation_key_expired(self):
        return now() > self.activation_key_expires

    @property
    def is_privileged(self):
        return self.is_staff or self.is_moderator or self.is_superuser

    @property
    def is_blocked(self):
        return now() < self.block_expires

    def block(self, hours):
        self.block_expires = now() + timedelta(hours=hours)
