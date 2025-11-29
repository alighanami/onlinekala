from django.db import models
from ckeditor.fields import RichTextField

from products.model.category import Category


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام')
    description = RichTextField(verbose_name='توضیحات')
    content = RichTextField(verbose_name='محتوا', default='')
    price = models.PositiveBigIntegerField(verbose_name='قیمت')
    stock = models.PositiveSmallIntegerField(verbose_name='موجودی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    image = models.ImageField(upload_to='static/sliders/', verbose_name='تصویر')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='یرایش')
    visit_count = models.PositiveIntegerField(default=0, verbose_name='بازدید')
    categories = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='دسته بندی')
    is_featured = models.BooleanField(default=False, verbose_name="نمایش دلخواه")
    product_type = models.CharField(max_length=100,blank=True,null=True,verbose_name="نوع محصول")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
