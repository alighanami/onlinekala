from django.contrib import admin

from orders.model.transaction import Transaction


class TransactionInlines(admin.TabularInline):
    model = Transaction
    fields = ('amount', 'status','payment_gateway')