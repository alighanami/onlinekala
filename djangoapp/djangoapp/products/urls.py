from django.urls import path, include

from rest_framework.routers import DefaultRouter

from products.view.api.category_view_set import CategoryViewSet
from products.view.api.product_view_set import ProductViewSet
from products.view.product_electric_cooler_list_view import ProductElectricCoolerListView
from products.view.product_electric_fridge_list_view import ProductElectricFridgeListView
from products.view.product_electric_vacuum_list_view import ProductElectricVacuumListView
from products.view.product_kitchen_cookware_list_view import ProductKitchenCookwareListView
from products.view.product_kitchen_decor_list_view import ProductKitchenDecorListView
from products.view.product_kitchen_gas_list_view import ProductKitchenGasListView
from products.view.product_laptop_gaming_list_view import ProductLaptopGamingListView
from products.view.product_laptop_office_list_view import ProductLaptopOfficeListView
from products.view.product_mobile_android_list_view import ProductMobileAndroidListView
from products.view.product_mobile_iphone_list_view import ProductMobileIphoneListView
from products.view.product_mobile_xiaomi_list_view import ProductMobileXiaomiListView
from products.view.product_view import ProductView
from products.view.search_view import SearchView

router = DefaultRouter()
router.register('', ProductViewSet)
router.register('categories', CategoryViewSet,basename='category')

urlpatterns = [
    path('api/products/', include(router.urls)),
    path('product/<int:pk>/', ProductView.as_view()),
    path('electric/cooler/', ProductElectricCoolerListView.as_view()),
    path('electric/fridge/', ProductElectricFridgeListView.as_view()),
    path('electric/vacuum/', ProductElectricVacuumListView.as_view()),
    path('mobile/xiaomi/', ProductMobileXiaomiListView.as_view()),
    path('mobile/android/', ProductMobileAndroidListView.as_view()),
    path('mobile/iphone/', ProductMobileIphoneListView.as_view()),
    path('laptop/gaming/', ProductLaptopGamingListView.as_view()),
    path('laptop/office/', ProductLaptopOfficeListView.as_view()),
    path('kitchen/gas/', ProductKitchenGasListView.as_view()),
    path('kitchen/cookware/', ProductKitchenCookwareListView.as_view()),
    path('kitchen/decor/', ProductKitchenDecorListView.as_view()),
    path('search/', SearchView.as_view(), name='search'),
]
