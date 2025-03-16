from . import views
from django.urls import path

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:product_id>/', views.product_detail, name='product-detail'),
    path('review/<int:product_id>/', views.product_review, name='product-review'),
    path('add_review/<int:product_id>', views.add_product_review, name='add-product-review'),
    path('search', views.search_product, name = 'search-product')
 
]

