import random
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from orders.model.order import Order
from orders.model.transaction import Transaction
from orders.model.basket import Basket
from orders.model.enumeration.payment_status import PaymentStatus


class VerifyView(View):
    def get(self, request):
        status = request.GET.get('status')
        order_pk = request.session.get('last_order_pk')

        if not order_pk:
            messages.error(request, "نشست شما منقضی شده یا سفارشی یافت نشد.", extra_tags='danger')
            return redirect('/')

        try:
            order = Order.objects.get(pk=order_pk)
            transaction = Transaction.objects.get(order=order)
        except (Order.DoesNotExist, Transaction.DoesNotExist):
            messages.error(request, "اطلاعات تراکنش یا سفارش نامعتبر است.", extra_tags='danger')
            return redirect('/')

        # ------------------- منطق اصلی -------------------
        if status == 'OK':
            fake_ref_id = random.randint(100000, 999999)

            order.status = PaymentStatus.PAID
            order.save()

            transaction.status = PaymentStatus.PAID
            transaction.ref_id = fake_ref_id
            transaction.save()

            Basket.objects.filter(user=request.user).delete()

            # حذف پیام‌های قبلی اگر مونده بودن و ثبت پیام واحد
            messages.get_messages(request).used = True
            messages.success(request, "پرداخت شما با موفقیت انجام و سفارش ثبت شد.", extra_tags='success')

            context = {
                'success': True,
                'order': order,
                'transaction': transaction,
            }
            return render(request, 'verify.html', context)

        else:
            order.status = PaymentStatus.FAILED
            order.save()

            transaction.status = PaymentStatus.FAILED
            transaction.save()

            messages.error(request, "پرداخت ناموفق بود یا توسط شما لغو شد.", extra_tags='danger')

            context = {
                'success': False,  # ✅ اصلاح‌شده
                'order': order,
                'transaction': transaction,
            }
            return render(request, 'verify.html', context)
