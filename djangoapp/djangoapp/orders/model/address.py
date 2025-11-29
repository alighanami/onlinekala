from django.contrib.auth.models import User
from django.db import models


class Address(models.Model):
    postal_code = models.CharField(max_length=10,verbose_name='کد پستی')
    mobile = models.CharField(max_length=15, unique=True,verbose_name='موبایل')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='address',verbose_name='کاربر')
    addr = models.CharField(max_length=4000, default='',verbose_name='آدرس')

    def __str__(self):
        return f"{self.user.username} {self.postal_code}"

    class Meta:
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس'
