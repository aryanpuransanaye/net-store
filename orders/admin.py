from django.contrib import admin
from .models import  Order, OrderItem, DiscountByCode


@admin.action(description = 'تغیر وضعیت به ارسال شده')
def make_sent(modeladmin, request, queryset):
    queryset.update(status='Shipped')

@admin.action(description = 'تغیر وضعیت به درانتظار')
def make_pending(modeladmin, request, queryset):
    queryset.update(status='Pending')


@admin.action(description = 'تغیر وضعیت به تحویل داده شده')
def make_delivered(modeladmin, request, queryset):
    queryset.update(status='Delivered')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    actions = [make_sent, make_pending, make_delivered]

    list_display = ['customer', 'total_price', 'created_at', 'status', 'final_price']
    readonly_fields = ['final_price']
    list_filter = ['status']
    search_fields = ['customer', 'status']
    list_per_page = 10

@admin.register(OrderItem)  
class OrderItemAdmin(admin.ModelAdmin):

    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order']
    search_fields = ['order']
    list_per_page = 10


@admin.register(DiscountByCode)
class DiscountByCodeAdmin(admin.ModelAdmin):

    list_display = ['discount_code', 'discount_percentage', 'start_date', 'end_date', 'used_count', 'max_usage']
    readonly_fields = ['used_count']
    list_filter = ['start_date', 'end_date']
    ordering = ['-start_date',]
