from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
    token = models.CharField(
        max_length=30,
        null=True)
    expires = models.DateTimeField(
        null=True)
    user = models.OneToOneField(
        User,
        related_name='auth_token',
        on_delete=models.CASCADE)

    class Meta:
        verbose_name = "User Token"
        verbose_name_plural = "User Tokens"

    def __str__(self):
        return "Token for user {} is {}".format(self.user, self.token)


class AppToken(models.Model):
    client_id = models.CharField(
        max_length=40)
    client_secret = models.CharField(
        max_length=128)
    token = models.CharField(
        max_length=30,
        blank=True,
        null=True)
    expires = models.DateTimeField(
        blank=True,
        null=True)

    class Meta:
        verbose_name = "App Token"
        verbose_name_plural = "App Tokens"

    def __str__(self):
        return "Token for client id {} is {}".format(self.client_id, self.token)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE)
    instagram_username = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        verbose_name="Instagram username")

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"

    def __str__(self):
        return "{}".format(self.user.username)