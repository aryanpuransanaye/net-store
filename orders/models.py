from django.db import models

class Order(models.Model):
    
    CHOICES = [
        ("Pending", "Pending"), 
        ("Shipped", "Shipped"), 
        ("Delivered", "Delivered")
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES, default="Pending") 

    def __str__(self):
        return f"Order #{self.id} - {self.customer.user.get_username()}"


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    def save(self, *args, **kwargs):
        
        if not self.price:
            self.price = self.product.price 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - {self.order.customer.user.get_username()}"
