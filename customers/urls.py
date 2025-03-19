from django.urls import path
from . import views

app_name = 'customers'

urlpatterns = [
    path('address-list/', views.address_list, name='address-list'),
    path('address-create/', views.address_create, name='address-create'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit-address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete-address'),
    path('address/set-active/<int:address_id>/', views.set_active_address, name='set-active-address'),
    path('wishlist-list/', views.wishlist_list, name='wishlist-list'),
    path('product-select/', views.product_select, name='product-select'),
    path('wishlist-add/<int:product_id>/', views.wishlist_add, name='wishlist-add'),
    path('wishlist-remove/<int:product_id>/', views.remove_from_wishlist, name= 'remove-from-wishlist'),
    path('customer-profile', views.customer_profile ,name = 'customer-profile'),
    path('edit-customer-profile', views.edit_customer_profile, name = 'edit-customer-profile')
]
 