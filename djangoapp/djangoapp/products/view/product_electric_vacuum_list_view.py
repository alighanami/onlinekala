from django.views.generic import ListView

from core.model.navigation import Navigation
from products.model.product import Product


class ProductElectricVacuumListView(ListView):
    model = Product
    template_name = 'product_electric_vacuum_list.html'
    context_object_name = 'products_vacuum'
    paginate_by = 3
    navigations = Navigation.objects.filter(is_active=True)
    extra_context = {
        'navigations': navigations
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(product_type='جاروبرقی')

