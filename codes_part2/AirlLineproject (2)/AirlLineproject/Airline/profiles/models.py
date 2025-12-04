from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    national_id = models.CharField(max_length=10, blank=True, null=True)

    wallet_balance = models.BigIntegerField(default=0, verbose_name="موجودی (تومان)")

    def __str__(self):
        return self.email