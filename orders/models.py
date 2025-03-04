from django.db import models
from customers.models import Customer
from products.models import Product


class Order(models.Model):

    CHOICES = [
        ("Pending", "Pending"), 
        ("Shipped", "Shipped"), 
        ("Delivered", "Delivered")]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 20, choices = CHOICES)

    def __str__(self):
        return self.customer.user.get_username()

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product
