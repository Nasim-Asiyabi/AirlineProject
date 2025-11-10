# reservations/models.py
from django.db import models
from django.conf import settings


class Reservation(models.Model):
    """مدل رزرو یا بلیط صادر شده (فاکتور فروش)"""

    class ReservationStatus(models.TextChoices):
        PURCHASED = 'PUR', 'خریداری شده'
        CANCELLED = 'CAN', 'کنسل شده'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="کاربر (خریدار)"
    )
    flight = models.ForeignKey(
        'flights.Flight',
        on_delete=models.PROTECT,
        verbose_name="پرواز (محصول)"
    )

    purchase_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ خرید"
    )

    purchased_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="قیمت در لحظه خرید"
    )

    status = models.CharField(
        max_length=3,
        choices=ReservationStatus.choices,
        default=ReservationStatus.PURCHASED,
        verbose_name="وضعیت رزرو"
    )

    def str(self):
        return f"رزرو {self.user.email} برای {self.flight}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.purchased_price = self.flight.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "رزرو (بلیط)"
        verbose_name_plural = "رزروها (بلیط‌ها)"