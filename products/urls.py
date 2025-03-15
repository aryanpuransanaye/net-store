from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:product_id>/', views.product_detail, name='product-detail'),
    path('review/<int:product_id>/', views.product_review, name='product-review'),
    path('add_review/<int:product_id>', views.add_product_review, name='add-product-review'),
    #path('brand/<int:brand_id>/', views.product_by_brand, name='product-by-brand'),
    #path('category/<int:category_id>/', views.product_by_category, name='product-by-category'),
    #path('tag/<int:tag_id>/', views.product_by_tag, name='product-by-tag'),
    path('sort-by/', views.filtered_products, name='sort-by')
]

