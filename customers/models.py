from django.db import models
from django.contrib.auth.models import User 

class Customer(models.Model):

    CHOISES = [
        ('active', 'Active'), 
        ('inactive', 'Inactive')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
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
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.city} - {self.state} - {self.postal_code}'
