from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View

from core.model.navigation import Navigation
from orders.model.order import Order


class IPGView(View):
    #این یعنی: “سلام! من دستگاه جادویی پرداخت اسباب‌بازی هستم!”


    def get(self, request: HttpRequest):
        #این یعنی: “وقتی یه بچه‌ی خوشحال (که همون request یا تو باشی) می‌رسه جلوی من، من این کارها رو براش انجام می‌دم:”


        order_pk = request.session['last_order_pk']
        #دستگاه جادویی اولین کاری که می‌کنه اینه که خیلی آروم و با لبخند دست می‌کنه توی جیب تو (request.session)
        # تا اون بلیت طلایی (last_order_pk) رو که صندوق‌دار بهت داده بود، پیدا کنه.
        # روی اون بلیت، شماره‌ی فاکتورت نوشته شده.


        if not order_pk:
#دستگاه با خودش فکر می‌کنه: “وایسا ببینم! نکنه این بچه بلیتش رو گم کرده باشه؟”
#این خط یعنی: “اگر دست کردم تو جیبش و هیچ بلیتی پیدا نکردم (if not order_pk)…”
            messages.error(request, 'سفارشی برای پرداخت یافت نشد', extra_tags='danger')
#… دستگاه یهو قیافش ناراحت می‌شه، یه چراغ قرمز روش روشن می‌شه (messages.error) و با یه صدای بامزه بهت می‌گه:
# “اوه! انگار فاکتورت رو گم کردی! بهتره برگردی دم در ورودی شهربازی (/) و دوباره بیای.
# ” و با یه سرسره کوچولو تو رو می‌فرسته به اول شهربازی.


            return redirect('/')

        order = get_object_or_404(Order, pk=order_pk)
#اما اگه بلیت توی جیبت باشه، دستگاه جادویی خوشحال می‌شه!
# شماره روی بلیت (order_pk) رو می‌خونه و یه ربات کوچولوی پرنده (get_object_or_404) رو صدا می‌زنه.
#بهش می‌گه: “هی ربات! برو به اتاق بایگانی فاکتورها (Order) و فاکتور شماره order_pk رو برای من پیدا کن و بیار!”
#این ربات خیلی دقیقه. اگه فاکتور رو پیدا نکنه، خیلی ناراحت می‌شه و ارور می‌ده (404 Not Found).
# ولی اگه پیداش کنه، کل پوشه‌ی فاکتور (order) رو که توش نوشته چی خریدی و قیمتش چنده، میاره و می‌ده به دستگاه.
        navigations = Navigation.objects.filter(is_active=True)
        context = {
            'navigations': navigations,
            'order': order
        }
        return render(request, 'ipg.html', context)

#کار دستگاه دیگه تقریباً تمومه! حالا یه نقاش جادویی (render) رو صدا می‌زنه.
#بهش می‌گه: “آقای نقاش! بیا اینا رو بگیر:”
#این بچه‌ی عزیز (request).
#این بوم نقاشی خالی که اسمش ipg.html هست.
#این سینی پر از وسیله (context).
#نقاش جادویی هم روی بوم نقاشی، یه عکس خیلی قشنگ برای تو می‌کشه.
# توی عکس، جزئیات فاکتورت (order) رو می‌نویسه تا ببینی برای چی داری پول می‌دی،
# و بالای صفحه هم اسم تابلوهای راهنما (navigations) رو می‌کشه تا اگه خواستی، بتونی دوباره تو شهربازی بگردی.
