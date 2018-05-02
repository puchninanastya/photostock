from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserPhotoInfo(models.Model):
    user = models.PositiveIntegerField(
        blank=False,
        null=False,
        verbose_name="Photo's owner id")
    added_at = models.DateTimeField(
        blank=True,
        null=False,
        auto_now_add=True,
        verbose_name="Datetime when photo was added")
    user_tags = ArrayField(
        models.CharField(max_length=200),
        blank=True,
        verbose_name="Photo's tags added by user")
    ai_tags = ArrayField(
        models.CharField(max_length=200),
        blank=True,
        verbose_name="Photo's tags automatically added by Artificial Intelligence")
    downloads = models.PositiveIntegerField(
        blank=True,
        null=False,
        default=0,
        verbose_name="Downloads of the photo")

    def __str__(self):
        return "Photo {}, owner with id {}".format(self.pk, self.user)
