from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=60)
    text = models.TextField()
    publish_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "статья"
        verbose_name_plural = "статьи"
