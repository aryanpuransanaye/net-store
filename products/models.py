from decimal import Decimal
from django.db import models
from django.db import models
from django.utils import timezone


class Category(models.Model):

    name = models.CharField(max_length=255, unique = True)
    description = models.TextField(blank = True, null = True)
    image = models.ImageField(null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    

    def __str__(self):
        return self.name


class Brand(models.Model):

    name = models.CharField(max_length=255, unique = True)
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to = 'brnad_image/', null = True, blank = True)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to = 'products_image/', null = True, blank = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete = models.CASCADE, null = True, blank=True)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    stock = models.IntegerField()
    description = models.TextField(blank=True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    final_price = models.DecimalField(max_digits = 10, decimal_places = 2, null = True, blank = True)
    discount_percentage = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(max_length=255, null = False, blank = False)
    product = models.ManyToManyField(Product)  
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name


class Review(models.Model):
    
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    user = models.ForeignKey('customers.Customer', on_delete = models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Review by {self.user.user.get_username()} for {self.product.name}'


class Discount(models.Model):

    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    discount_percentage = models.FloatField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.product.name} - {self.discount_percentage}%"
 