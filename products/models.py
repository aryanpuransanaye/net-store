from django.db import models
from decimal import Decimal
from django.utils import timezone


class Category(models.Model):

    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Brand(models.Model):

    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null = True, blank = True) 

    def __str__(self):
        return self.name

    def update_final_price(self):
       
        discount = Discount.objects.filter(
            product=self, 
            start_date__lte=timezone.now(), 
            end_date__gte=timezone.now()
        ).first()

        if discount:  
        
            discount_amount = Decimal(str(discount.discount_percentage)) / Decimal('100')
            self.final_price = self.price * (Decimal('1') - discount_amount)
        else:
            self.final_price = self.price

        self.save()


class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.product.name} - {self.discount_percentage}%"