from django.views.generic import ListView
from django.db.models import Q

from core.model.navigation import Navigation
from products.model.product import Product


class SearchView(ListView):
    template_name = 'search.html'
    model = Product
    context_object_name = 'products'  # تو html با این اسم صداش می‌زنیم

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # جستجو در نام و توضیحات
            return Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        return Product.objects.none()  # اگه خالی بود هیچی نیار

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # این رو میذاریم تا نوبار توی صفحه سرچ هم کار کنه
        context['navigations'] = Navigation.objects.filter(is_active=True)
        # کلمه سرچ شده رو برمی‌گردونیم که تو تایتل نشون بدیم
        context['query'] = self.request.GET.get('q')
        return context
