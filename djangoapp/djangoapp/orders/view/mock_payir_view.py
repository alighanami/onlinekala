# orders/view/mock_payir_view.py

from django.shortcuts import render  # render رو ایمپورت کن
from django.views import View

class MockPayirView(View):
    def get(self, request):
        """
        این ویو صفحه درگاه پرداخت جعلی را برای کاربر نمایش می‌دهد.
        """
        # توکنی که از ویوی قبلی فرستاده شده رو میگیریم (اختیاری)
        token = request.GET.get('token')

        context = {
            'token': token,
        }
        # به جای redirect، صفحه html جدید رو رندر می‌کنیم
        return render(request, 'mock_gateway.html', context)
