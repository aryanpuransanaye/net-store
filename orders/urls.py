from django.urls import path
from .views import (
    CustomerOrderView, AddToCartView, RemoveOrderItemView, RemoveOrderView, ApplyDiscountView
)

app_name = 'orders'

urlpatterns = [
    path('orders/', CustomerOrderView.as_view(), name='orders'),
    path('orders/<int:order_id>/', CustomerOrderView.as_view(), name='order-detail'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('cart/remove-order/<int:order_id>/', RemoveOrderView.as_view(), name='remove-order'),
    path('order/<int:order_id>/remove-item/<int:item_id>/', RemoveOrderItemView.as_view(), name='remove-order-item'),
    path('apply-discount/<int:order_id>/', ApplyDiscountView.as_view(), name='apply-discount'),
]