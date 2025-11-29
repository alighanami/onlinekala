from django.urls import path

from orders.view.add_to_basket_view import AddToBasketView
from orders.view.basket_view import BasketView
from orders.view.ipg_view import IPGView
from orders.view.mock_payir_view import MockPayirView
from orders.view.payment_view import PaymentView
from orders.view.register_view import RegisterView
from orders.view.remove_from_basket_view import RemoveFromBasketView
from orders.view.update_quantity_view import UpdateQuantityView
from orders.view.verify_view import VerifyView

urlpatterns = [
    path('basket/<int:product_id>/add/', AddToBasketView.as_view()),
    path('basket/', BasketView.as_view(), name='basket_summary'),
    # برای اینکه در صفحات حذف یا کم و زیاد ایتم ها ریدایرکت عمل کنه حتما باید name بزاریم که عمل کنه

    path('basket/update/<int:item_id>/', UpdateQuantityView.as_view(), name='update_quantity_basket'),
    path('basket/remove/<int:item_id>/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
    path('register/', RegisterView.as_view()),
    path('ipg/', IPGView.as_view()),
    path('pay/', PaymentView.as_view()),
    path('verify/', VerifyView.as_view()),
    path('mock-payir/', MockPayirView.as_view(), name='mock_payir'),

]
