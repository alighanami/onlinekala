from django.contrib import admin

from orders.model.admin.order_item_admin import OrderItemAdmin
from orders.model.admin.transaction_admin import TransactionInlines
from orders.model.order import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('user', 'status',)
    inlines =[OrderItemAdmin,TransactionInlines]

    def get_queryset(self, request):
        qs=super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

#نقطه (.) فقط یه جداکننده است که میگه «از چیزی که در سمت چپم هست،
# چیزی که در سمت راستم هست رو برام پیدا کن».

