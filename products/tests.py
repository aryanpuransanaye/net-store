from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product, Brand, Category, Review, Discount
from customers.models import Customer
from django.contrib.auth.models import User
from decimal import Decimal
from django.utils import timezone

class ProductViewsTest(TestCase):

    def setUp(self):
        
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.customer = Customer.objects.create(user=self.user)
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="BrandX")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            brand=self.brand,
            price=1000.0,
            stock=10,
            description="Test Description"
        )

    def test_home_view(self):
        
        response = self.client.get(reverse("products:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_search_product_view(self):
     
        response = self.client.get(reverse("products:search-product"), {"q": "Test"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail_view(self):
       
        response = self.client.get(reverse("products:product-detail", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_review_view(self):
       
        Review.objects.create(product=self.product, user=self.customer, rating=5, comment="Great product!")
        response = self.client.get(reverse("products:product-review", args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Great product!")

    def test_add_product_review_view(self):
       
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("products:add-product-review", args=[self.product.id]), {
            "rating": 5,
            "comment": "Amazing product!"
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Review.objects.filter(product=self.product, user=self.customer, comment="Amazing product!").exists())