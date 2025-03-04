from django.contrib import admin
from .models import Customer, Address


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'status')


@admin.register(Address)  
class AddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'city', 'state', 'postal_code', 'created_at')
