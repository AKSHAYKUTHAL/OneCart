from django.contrib import admin
from .models import Product, ProductColor, ProductSize

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'category', 'product_price', 'product_stock', 'product_is_available']
    filter_horizontal = ['product_colors', 'product_sizes']  # Use filter_horizontal for many-to-many fields
    list_filter = ('category','product_is_available')
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSize)
admin.site.register(ProductColor)
