from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('customers/', include('customers.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', include('products.urls')),
]
