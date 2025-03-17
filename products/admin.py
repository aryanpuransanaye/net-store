from django.contrib import admin
from django.db.models import Q
from .models import Discount, Product, Brand, Category, Tag, Review



@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['product', 'discount_percentage', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
    ordering = ['-start_date',]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ['name', 'brand', 'category', 'price', 'final_price', 'discount_percentage']
    readonly_fields = ['final_price', 'discount_percentage']
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


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ['name', 'get_products', 'created_at']
    search_fields = ['name']
    ordering = ['-name',]

    def get_products(self, obj):
        return ", ".join([product.name for product in obj.product.all()]) 
    get_products.short_description = 'Products'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = ['get_customer_username', 'get_products', 'rating', 'comment' ,'created_at']
    search_fields = ['get_search_result']
    ordering = ['product',]

    
    def get_customer_username(self, obj):

        return obj.user.user.username 
    get_customer_username.short_description = 'Customer Username' 

    def get_products(self, obj):

        return obj.product.name
    get_products.short_description = 'Products'

    
    def get_search_result(self, request, queryset, search_term):

        query = request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(customer__user__username__icontains=query) | Q(product__name__icontains=query)
            )
        return queryset, False
    



