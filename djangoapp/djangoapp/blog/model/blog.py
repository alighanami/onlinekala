from django.db import models
from ckeditor.fields import RichTextField


class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name='عنوان')
    sub_title=models.CharField(max_length=255,default='',verbose_name='زیرعنوان')
    content = RichTextField(verbose_name='محتوا')
    image = models.ImageField(upload_to='static/sliders/', verbose_name='تصویر')
    is_published = models.BooleanField(default=True, verbose_name='منتشرشده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='ویرایش')
    visit_count = models.PositiveIntegerField(default=0, verbose_name='بازدید')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بلاگ'
        verbose_name_plural = 'بلاگ'
