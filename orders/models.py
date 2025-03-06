from django.db import models


class Order(models.Model):

    CHOICES = [
        ("Pending", "Pending"), 
        ("Shipped", "Shipped"), 
        ("Delivered", "Delivered")]

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 20, choices = CHOICES)

    def __str__(self):
        return self.customer.user.get_username()

class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='order_item_image/', null=True, blank=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product
