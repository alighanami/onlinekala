# orders/view/payment_view.py

import uuid
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.views import View

from orders.model.basket import Basket
from orders.model.order import Order
from orders.model.order_item import OrderItem
from orders.model.transaction import Transaction


class PaymentView(View):
    def get(self, request: HttpRequest):
        if not request.user.is_authenticated:
            messages.error(request, 'لطفا ابتدا وارد حساب کاربری خود شوید', extra_tags='danger')
            return redirect('/')

        basket_items = Basket.objects.filter(user=request.user)

        if not basket_items.exists():
            messages.error(request, 'سبد خرید شما خالی است', extra_tags='danger')
            # بهتر است به صفحه سبد خرید بازگردد تا صفحه اصلی
            return redirect('orders:basket')  # فرض بر این است که اسم URL سبد خرید شما 'basket' است

        # ۱. محاسبه مبلغ کل
        total_price = sum(item.get_total_price() for item in basket_items)

        # ۲. ایجاد سفارش و آیتم‌های آن در دیتابیس
        order = Order.objects.create(user=request.user, amount=total_price)
        for item in basket_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # ۳. ایجاد تراکنش اولیه برای این سفارش
        Transaction.objects.create(
            order=order,
            amount=total_price,
            payment_gateway='MockGateway'  # نام درگاه را به درگاه تستی تغییر دادیم
        )

        # ۴. ذخیره شماره سفارش (PK) در سشن. این مهم‌ترین بخش برای مرحله تایید است.
        request.session['last_order_pk'] = order.pk

        # ۵. ایجاد یک توکن ساختگی برای ارسال به درگاه جعلی
        fake_token = str(uuid.uuid4())

        # ۶. هدایت کاربر به صفحه درگاه پرداخت جعلی (MockPayirView)
        # این URL باید با چیزی که در orders/urls.py تعریف کرده‌اید مطابقت داشته باشد
        return redirect(f'/mock-payir/?token={fake_token}')