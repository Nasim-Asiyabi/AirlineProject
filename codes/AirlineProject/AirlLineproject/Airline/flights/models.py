# flights/models.py
from django.db import models


class Airport(models.Model):
    """مدل برای «مدیریت فرودگاه‌ها»"""
    name = models.CharField(max_length=100, verbose_name="نام شهر/فرودگاه")
    code = models.CharField(
        max_length=3,
        unique=True,
        help_text="کد 3 حرفی اختصاصی (مثلا THR)",
        verbose_name="کد اختصاصی"
    )

    def str(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "فرودگاه"
        verbose_name_plural = "فرودگاه‌ها"


class Airline(models.Model):
    """مدل برای «مدیریت شرکت‌های هواپیمایی»"""
    name = models.CharField(max_length=100, verbose_name="نام شرکت هواپیمایی")

    def str(self):
        return self.name

    class Meta:
        verbose_name = "شرکت هواپیمایی"
        verbose_name_plural = "شرکت‌های هواپیمایی"


class Route(models.Model):
    """مدل برای «مدیریت مسیرها» (ترکیب مبدأ و مقصد)"""
    origin = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_from",
        verbose_name="مبدأ"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_to",
        verbose_name="مقصد"
    )

    def str(self):
        return f"{self.origin.code} به {self.destination.code}"

    class Meta:
        verbose_name = "مسیر"
        verbose_name_plural = "مسیرها"
        unique_together = ('origin', 'destination')  # یک مسیر نباید تکراری باشد


class Flight(models.Model):
    """مدل برای «مدیریت برنامه پروازی» (موجودی انبار)"""
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name="مسیر")
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE, verbose_name="شرکت پروازی")

    departure_time = models.DateTimeField(verbose_name="تاریخ و ساعت پرواز")
    arrival_time = models.DateTimeField(verbose_name="تاریخ و ساعت رسیدن")

    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت")

    total_seats = models.PositiveIntegerField(verbose_name="ظرفیت کل صندلی")
    available_seats = models.PositiveIntegerField(verbose_name="صندلی‌های باقیمانده")

    cancellation_fee_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.20,
        help_text="مثلا 0.20 برای ۲۰ درصد جریمه",
        verbose_name="درصد جریمه کنسلی"
    )

    def str(self):
        return f"پرواز {self.route} در {self.departure_time}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "پرواز"
        verbose_name_plural = "پروازها"
        ordering = ['departure_time']