from django.contrib import admin

from products.model.product import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','name','price','stock','is_active','created_at','visit_count','is_featured','product_type',)
    list_filter = ('is_active','created_at','updated_at','product_type',)
    search_fields = ('name','description',)
    list_editable = ('price','stock','is_active','is_featured','product_type',)