from rest_framework.viewsets import ReadOnlyModelViewSet

from products.model.product import Product
from products.model.serializer.category_serializer import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = CategorySerializer