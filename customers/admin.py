from django.contrib import admin
from django.db.models import Q
from .models import Customer, Address, Wishlist


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'phone', 'created_at', 'status')


@admin.register(Address)  
class AddressAdmin(admin.ModelAdmin):

    list_display = ('customer', 'city', 'state', 'postal_code', 'created_at')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = ('get_customer_username', 'get_products', 'creat_at')
    search_fields = ['product__name', 'customer__user__username']


    def get_customer_username(self, obj):

        return obj.customer.user.username 
    get_customer_username.short_description = 'Customer Username' 

    def get_products(self, obj):

        return ", ".join([product.name for product in obj.product.all()])
    get_products.short_description = 'Products'


    def get_search_result(self, request, queryset, search_term):

        query = request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(customer__user__username__icontains=query) | Q(product__name__icontains=query)
            )
        return queryset, False
