'''
این کد مثل یه کارگر ماهر توی سبد خرید شماست. اسم این کارگر UpdateQuantityView هست.
 وظیفه‌اش اینه که وقتی شما توی صفحه سبد خرید، تعداد یه محصول رو کم و زیاد می‌کنی یا یه عدد جدید وارد می‌کنی،
  اون بیاد و سبد شما رو دقیقاً طبق دستور شما به‌روز کنه.
بریم ببینیم این کارگر چطور کار می‌کنه.
'''



from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from orders.model.basket import Basket
from orders.util.basket_util import get_guest_id


class UpdateQuantityView(View):
#کارگر ما، UpdateQuantityView، یونیفرمش رو می‌پوشه و آماده به کار می‌ایسته. اون فقط منتظر یه دستوره.



    def post(self, request, item_id):
        #وقتی دکمه رو می‌زنی، کارگر ما سه تا چیز دریافت می‌کنه:
        #self: خودِ کارگر.
        #request: شما، یعنی مشتری با تمام اطلاعاتت.
        #item_id: شماره یا کد اون محصولی که می‌خوای تعدادش رو تغییر بدی.

        try:

            basket_item = self._get_basket_item_by_id(request, item_id)
            #قبل از هر کاری، کارگر ما یه دستیار تیز و فرز داره به اسم _get_basket_item_by_id.
            # به این دستیار میگه: “برو آیتمی با این شماره (item_id) که مال همین مشتری (request) هست رو پیدا کن و بیار.”
            #این دستیار خیلی مهمه چون جلوی دو تا اشتباه بزرگ رو می‌گیره:
            #مطمئن می‌شه که آیتم اصلاً وجود داره.
            #مطمئن می‌شه که شما داری آیتم توی سبد خودت رو تغییر می‌دی، نه سبد یه مشتری دیگه! (این خیلی امنیتیه).
            # اگه شما لاگین کرده باشی، با user چک می‌کنه. اگه مهمان باشی، با guest_id چک می‌کنه.



            action = request.POST.get('action')
#همونطور که گفتیم، request مثل یک نامه یا بسته پستی است که مرورگر شما (مشتری) به سرور ما (فروشگاه) می‌فرسته.
# توی این بسته همه چیز هست: آدرس فرستنده، مقصد نامه، و از همه مهم‌تر، محتویات نامه.
#وقتی شما دکمه‌ای رو در یک فرم HTML می‌زنید که متدش POST هست،
# تمام اطلاعات اون فرم، داخل یک بخش مخصوص از نامه به اسم POST قرار می‌گیره.
#request.POST مثل یک دیکشنری پایتون عمل می‌کنه. کلیدهای این دیکشنری،
# nameهای فیلدهای فرم شما هستن و مقادیرش، valueهایی هستن که اون فیلدها داشتن.
#بخش سوم و مهم‌ترین بخش: .get('action') (خواندن یک دستور کار پنهان)
#اینجاست که جادو اتفاق میفته!

#.get('action') داره به پایتون میگه: “برو توی اون دیکشنری request.POST و دنبال کلیدی به اسم 'action' بگرد و مقدارش رو به من بده.”

#سوال اصلی اینه: این 'action' از کجا اومده؟ ما که توی فرممون فیلدی به اسم action نداشتیم که کاربر پر کنه!

#جواب اینه: ما این دستور کار رو به صورت یک فیلد مخفی (hidden input) توی فرم‌هامون جاسازی می‌کنیم!
            '''
            <!-- آیتم شماره ۱۲ در سبد خرید -->
<span>نام محصول: کتاب جنگو</span>
<span>تعداد: ۲</span>

<!-- فرم برای دکمه افزایش (+) -->
<form action="/update-quantity/12/" method="POST">
    {% csrf_token %}
    <input type="hidden" name="action" value="increase">
    <button type="submit">+</button>
</form>

<!-- فرم برای دکمه کاهش (-) -->
<form action="/update-quantity/12/" method="POST">
    {% csrf_token %}
    <input type="hidden" name="action" value="decrease">
    <button type="submit">-</button>
</form>
تحلیل کد بالا:

ما دو تا دکمه داریم: + و -.
هر دکمه داخل یک فرم جداگانه است.
فرم دکمه +، یک فیلد مخفی داره: <input type="hidden" name="action" value="increase">.
فرم دکمه -، یک فیلد مخفی مشابه داره: <input type="hidden" name="action" value="decrease">.
حالا سناریو رو ببین:

وقتی شما روی دکمه + کلیک می‌کنی:

فرم اولی ارسال می‌شه.

request.POST این شکلی می‌شه: {'action': 'increase', ...}

در نتیجه، request.POST.get('action') مقدار 'increase' رو برمی‌گردونه.

و کد ما وارد این شرط می‌شه: if action == 'increase':

وقتی شما روی دکمه - کلیک می‌کنی:

فرم دومی ارسال می‌شه.

request.POST این شکلی می‌شه: {'action': 'decrease', ...}

در نتیجه، request.POST.get('action') مقدار 'decrease' رو برمی‌گردونه.

و کد ما وارد این شرط می‌شه: elif action == 'decrease':

چرا از .get() استفاده می‌کنیم و نه از []؟
این یک نکته حرفه‌ایه. ما می‌تونستیم اینطوری هم بنویسیم: request.POST['action']

تفاوتش اینه:

request.POST['action']: مثل یه رئیس بداخلاق می‌مونه. اگه بره توی دیکشنری و کلید 'action' رو پیدا نکنه، داد و بیداد می‌کنه و کل برنامه با ارور KeyError متوقف می‌شه (Crash می‌کنه).
request.POST.get('action'): مثل یه کارمند مؤدب می‌مونه. اگه بره توی دیکشنری و کلید 'action' رو پیدا نکنه، خیلی آروم و بی‌صدا مقدار None (یعنی هیچی) رو برمی‌گردونه و برنامه به کارش ادامه می‌ده. این روش خیلی امن‌تره.
خلاصه کل داستان:

request.POST.get('action') یعنی: “برو توی فرمی که مشتری فرستاده، دنبال یه دستور کار مخفی به اسم
‘action’ بگرد و ببین چی نوشته. نوشته ‘increase’ یا ‘decrease’؟ تا من بدونم باید تعداد رو زیاد کنم یا کم.”



autorenew

thumb_up

thumb_down

            '''




            new_quantity = request.POST.get('quantity')

            if action == 'increase':
                basket_item.quantity += 1
                messages.success(request, f"تعداد {basket_item.product.name} افزایش یافت.")

            elif action == 'decrease':
                if basket_item.quantity > 1:
                    basket_item.quantity -= 1
                    messages.success(request, f"تعداد {basket_item.product.name} کاهش یافت.")
                else:
                    basket_item.delete()
                    messages.info(request, f"محصول {basket_item.product.name} از سبد حذف شد.")

            elif action == 'set' and new_quantity and new_quantity.isdigit():
                quantity_val = int(new_quantity)
                if quantity_val > 0:
                    basket_item.quantity = quantity_val
                    messages.success(request, f"تعداد {basket_item.product.name} به {quantity_val} تنظیم شد.")
                else:
                    basket_item.delete()
                    messages.info(request, f"محصول {basket_item.product.name} از سبد حذف شد (تعداد صفر وارد شد).")

            else:
                messages.error(request, "پارامتر به‌روزرسانی نامعتبر است.")
                return redirect('basket_summary')
#کارگر بعد از اینکه آیتم رو پیدا کرد، از روی فرمی که شما پر کردی، دستور کار (action) رو می‌خونه.

#اگر دستور increase بود: یکی به تعداد فعلی اضافه می‌کنه (quantity += 1) و با بلندگو اعلام می‌کنه: “یکی اضافه شد!”.
#اگر دستور decrease بود: اینجا یه کم باهوش‌تره.
#نگاه می‌کنه، اگه تعداد بیشتر از یکی بود، یکی کم می‌کنه (quantity -= 1).
#اما اگه فقط یکی مونده بود و شما دوباره “کاهش” رو زدی، دیگه تعداد رو صفر نمی‌کنه.
 # کل محصول رو از سبد حذف می‌کنه (basket_item.delete()) و با بلندگو میگه: “این محصول کلاً از سبد حذف شد!”.
#اگر دستور set بود: یعنی شما خودت یه عدد تایپ کردی.
#کارگر اول چک می‌کنه که آیا عدد درسته (isdigit).
#اگه عدد بزرگتر از صفر بود، تعداد رو به همون عدد تغییر می‌ده.
#اگه عدد صفر یا منفی بود، مثل حالت قبل، کل محصول رو از سبد حذف می‌کنه.


            basket_item.save()
            #تا اینجای کار، همه تغییرات فقط روی کاغذ و توی ذهن کارگر بود. این خط کد مثل زدنِ مهر “ثبت شود” است.
            # کارگر تغییرات جدید (تعداد جدید) رو توی سیستم انبارداری (پایگاه داده) برای همیشه ثبت می‌کنه.


        except Basket.DoesNotExist:
            messages.error(request, "آیتم مورد نظر در سبد شما یافت نشد.")
        return redirect('basket_summary')
        #این try-except مثل یه ناظر باتجربه بالای سر کارگر ایستاده.
        # اگه دستیارِ کارگر در همون مرحله اول نتونه آیتم رو پیدا کنه (مثلاً چون قبلاً حذف شده)،
        # این ناظر سریعاً جلوی کار رو می‌گیره، یه پیام خطا با بلندگو اعلام می‌کنه و اجازه نمی‌ده برنامه خراب بشه.
        #مهم نیست چه اتفاقی افتاد (افزایش، کاهش، حذف یا حتی خطا)، در نهایت کارگر کارش با اون آیتم تموم شده.
        # پس با تابلوی راهنما (redirect) به شما میگه: “خب، برگرد به صفحه اصلی سبد خرید (basket_summary) تا نتیجه رو ببینی.”

#و شما به صفحه سبد خرید برمی‌گردی و می‌بینی که همه چیز دقیقاً همونطور که خواسته بودی تغییر کرده. تمام! :)




    def _get_basket_item_by_id(self, request, item_id):
        if request.user.is_authenticated:
            return get_object_or_404(Basket, id=item_id, user=request.user)

        guest_id = get_guest_id(request)

        return get_object_or_404(Basket, id=item_id, guest_id=guest_id)
#فکر کن UpdateQuantityView همون کارگر ماهر ماست. این کارگر برای اینکه کارش رو تمیز و مرتب انجام بده،
# یه دستیار شخصی و متخصص برای خودش استخدام کرده. اسم این دستیار _get_basket_item_by_id هست.
#این _ که اول اسمش اومده، مثل یه قرارداد و قانون نانوشته بین برنامه‌نویس‌هاست.
# وقتی ما اول اسم یه چیزی _ می‌ذاریم، داریم به بقیه (و به خودمون در آینده!) می‌گیم:

#“هی! این دستیار، یه نیروی داخلی و محرمانه است.
# فقط و فقط خودِ کارگر اصلی (UpdateQuantityView) حق داره بهش دستور بده.
# لطفاً از بیرون این کلاس، کسی مزاحم این دستیار نشه!”
#پس این _ یک جور علامت “ورود ممنوع” برای دیگران و “فقط برای استفاده داخلی” برای خود کلاس است.