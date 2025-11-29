from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from orders.model.basket import Basket
from orders.util.basket_util import get_guest_id


class RemoveFromBasketView(View):
    """
    یک آیتم کامل را از سبد خرید حذف می‌کند.
    """

    def post(self, request, item_id):
        try:
            basket_item = self._get_basket_item_by_id(request, item_id)
            product_name = basket_item.product.name

            basket_item.delete()

            messages.success(request, f"محصول '{product_name}' با موفقیت از سبد حذف شد.")

        except Basket.DoesNotExist:
            messages.error(request, "آیتم مورد نظر برای حذف در سبد یافت نشد.")

        # ریدایرکت به صفحه سبد خرید
        return redirect('basket_summary')

        # از متد کمکی مشترک در بالا استفاده می‌شود

    def _get_basket_item_by_id(self, request, item_id):
        if request.user.is_authenticated:
            return get_object_or_404(Basket, id=item_id, user=request.user)

        guest_id = get_guest_id(request)

        return get_object_or_404(Basket, id=item_id, guest_id=guest_id)
