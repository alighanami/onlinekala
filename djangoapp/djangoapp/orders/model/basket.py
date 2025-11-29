from django.contrib.auth.models import User
from django.db import models

from products.model.product import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,verbose_name='کاربر')
    guest_id = models.CharField(max_length=255, null=True, blank=True,verbose_name='کاربرمهمان')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,verbose_name='محصول')
    quantity = models.PositiveSmallIntegerField(default=0,verbose_name='تعداد')
    added_at = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ اضافه شدن به سبد خرید')

    def __str__(self):
        if self.user:
            return f"{self.product.name} in basket of {self.user}"
        return f"{self.product.name} in basket of {self.guest_id}"

    def get_total_price(self):
        return self.quantity * self.product.price
