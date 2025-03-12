from django.urls import path
from .views import address_list, address_create, edit_address, delete_address, wishlist_list, wishlist_add, product_select

app_name = 'customers'

urlpatterns = [
    path('address-forms/', address_list, name='address-forms'),
    path('address-create/', address_create, name='address-create'),
    path('edit-address/<int:address_id>/', edit_address, name='edit-address'),
    path('delete-address/<int:address_id>/', delete_address, name='delete-address'),
    path('wishlist-list/', wishlist_list, name='wishlist-list'),
    path('product-select/', product_select, name='product-select'),
    path('wishlist-add/<int:product_id>/', wishlist_add, name='wishlist-add'),
]
