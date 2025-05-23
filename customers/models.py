from django.db import models
from django.contrib.auth.models import User 


class Customer(models.Model):

    CHOISES = [
        ('active', 'Active'), 
        ('inactive', 'Inactive')
        ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to = 'customer_profile_image/', null = True, blank = True)
    phone = models.CharField(max_length=15, unique=True, null= True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='active', choices = CHOISES)
    
    def __str__(self):
        return self.user.get_username()


class Address(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city} - {self.state} - {self.postal_code}'


class Wishlist(models.Model):

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField('products.Product')
    creat_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist of {self.customer.user.username}"