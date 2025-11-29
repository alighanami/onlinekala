from django.contrib import admin

from orders.model.order_item import OrderItem


class OrderItemAdmin(admin.StackedInline):
    model = OrderItem
    fields = ('product', 'quantity', 'price')
