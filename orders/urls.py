from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order-list/', views.customer_orders, name='customer-orders'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order-detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('remove-order/<int:order_id>/', views.remove_order, name='remove-order'),
    path('apply-discount/<int:order_id>/', views.apply_discount, name='apply-discount'),
    path('order/<int:order_id>/remove-item/<int:item_id>/', views.remove_order_item, name='remove-order-item'),

]
