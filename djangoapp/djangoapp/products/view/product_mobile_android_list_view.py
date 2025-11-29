from django.views.generic import ListView

from core.model.navigation import Navigation
from products.model.product import Product


class ProductMobileAndroidListView(ListView):
    model = Product
    template_name = 'product_mobile_android_list.html'
    context_object_name = 'products_android'
    paginate_by = 3
    navigations = Navigation.objects.filter(is_active=True)
    extra_context = {
        'navigations': navigations
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(product_type='موبایل-اندروید')

