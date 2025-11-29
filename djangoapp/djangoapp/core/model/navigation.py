from django.db import models


class Navigation(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    link = models.CharField(max_length=300)  # ✅ بدون validation اجباری
    is_active = models.BooleanField(default=True, verbose_name='فعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لینک'
        verbose_name_plural = 'لینک‌ها'
