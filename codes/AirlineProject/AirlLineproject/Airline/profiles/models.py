# profiles/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
# این دو خط را حتما اضافه کنید
from django.contrib.auth.models import Group, Permission
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(unique=True, verbose_name="ایمیل")

    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="شماره تلفن")
    national_id = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name="کد ملی")

    wallet_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name="موجودی کیف پول"
    )

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="profile_user_groups"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="profile_user_permissions"
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def str(self):
        return self.email

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        CHARGE = 'CHG', 'شارژ حساب'
        PURCHASE = 'PUR', 'خرید بلیط'
        REFUND = 'REF', 'بازگشت (کنسلی)'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="کاربر"
    )

    transaction_type = models.CharField(max_length=3, choices=TransactionType.choices, verbose_name="نوع تراکنش")
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="مبلغ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ و زمان")

    def str(self):
        return f"{self.user.username} - {self.get_transaction_type_display()} - {self.amount}"

    class Meta:
        verbose_name = "تراکنش مالی"
        verbose_name_plural = "تراکنش‌های مالی"
        ordering = ['-created_at']