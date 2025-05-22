from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


from .managers import UserManager


class User(AbstractUser):
    telegram_username = models.CharField(
        _("Telegram username"), max_length=255, unique=True, null=True, blank=True
    )
    telegram_id = models.BigIntegerField(
        _("Telegram id"), unique=True, db_index=True, null=True, blank=True
    )
    phone_number = models.CharField(
        _("Telegram phone number"), max_length=32, unique=True, null=True, blank=True
    )
    telegram_language = models.CharField(
        _("Telegram language code"), max_length=255, null=True, blank=True
    )
    referral = models.ForeignKey(
        "User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="referrals",
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    objects = UserManager()
