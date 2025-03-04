from django.contrib import admin
from .models import Discount, Product, Brand, Category


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):

    list_display = ['product', 'discount_percentage', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    ordering = ['-start_date',]
    def save_model(self, request, obj, form, change):
   
        super().save_model(request, obj, form, change)
        if obj.product:
            obj.product.update_final_price() 


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'brand', 'category', 'price', 'final_price']
    search_fields = ['name', 'brand', 'category', 'price', 'discount']
    list_filter = ['brand', 'category', 'price', 'discount']
    ordering = ['-name',]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['-name',]


@admin.register(Category)
class categoryAdmin(admin.ModelAdmin):

    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['-name',]  

