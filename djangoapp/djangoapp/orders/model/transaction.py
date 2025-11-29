from django.db import models

from orders.model.enumeration.payment_status import PaymentStatus
from orders.model.order import Order


class Transaction(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING,
        related_name='transactions',
        verbose_name='سفارش'  # این بهتره چون در واقع به Order وصله نه به User
    )
    amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name='مبلغ نهایی')
    status = models.CharField(
        max_length=10,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name='وضعیت'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    payment_gateway = models.CharField(max_length=50, default='ZarinPal', verbose_name='درگاه پرداخت')
    authority = models.CharField(max_length=255, default='', verbose_name='کد Authority')
    ref_id = models.CharField(max_length=128, blank=True, null=True)


    def __str__(self):
        return f"x{self.pk} {self.status}"

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
