from django.db import models
from django.utils import timezone
from decimal import Decimal

class Order(models.Model):
    
    CHOICES = [
        ("Pending", "Pending"), 
        ("Shipped", "Shipped"), 
        ("Delivered", "Delivered")
    ]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=True, blank=True)
    discount_code = models.ForeignKey('DiscountByCode', null=True, blank=True, on_delete=models.SET_NULL)
    discount_percentage = models.FloatField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=CHOICES, default="Pending")

    def update_total_price(self):
       
        total_price = sum(item.quantity * item.product.final_price for item in self.items.all())  

        self.total_price = total_price  
        if self.discount_percentage:
            discount_percentage = Decimal(self.discount_percentage) / Decimal(100)
            discount_amount = self.total_price * discount_percentage
            self.final_price = self.total_price - discount_amount
        else:
            self.final_price = self.total_price  

        return self.total_price 

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

class DiscountByCode(models.Model):

    discount_code = models.CharField(max_length=50, unique=True) 
    discount_percentage = models.FloatField() 
    start_date = models.DateTimeField()  
    end_date = models.DateTimeField() 
    max_usage = models.IntegerField(default=1)  
    used_count = models.IntegerField(default=0) 

    def is_valid(self):
        
        return (
            self.start_date <= timezone.now() <= self.end_date and
            self.used_count < self.max_usage
        )

    def __str__(self):
        return f"{self.discount_code} - {self.discount_percentage}% Discount"