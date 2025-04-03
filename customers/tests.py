from django.test import TestCase, Client
from django.contrib.auth.models import User
from customers.models import Customer, Address, Wishlist
from django.urls import reverse
from products.models import Product, Category, Brand

class CustomerViewsTest(TestCase):

    def setUp(self):
       
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.customer = Customer.objects.create(user=self.user, phone="09018173285", status="Active")
        self.category = Category.objects.create(name="Test Category")
        self.brand = Brand.objects.create(name="Test Brand")

    def test_customer_profile_view(self):
       
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("customers:customer-profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.customer.phone)

    def test_edit_customer_profile_view(self):
        
        self.client.login(username="testuser", password="password123")

        with open("C:/Users/aryan/OneDrive/Pictures/photo_2025-01-01_14-58-11.jpg", 'rb') as img:
            response = self.client.post(reverse("customers:edit-customer-profile"), {"customer_profile": img, 
                                                                            "phone": "09018173285"})
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.phone, "09018173285")

    def test_address_list_view(self):
        
        self.client.login(username="testuser", password="password123")
        Address.objects.create(customer=self.customer, city="Tehran")
        response = self.client.get(reverse("customers:address-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tehran")

    def test_address_create_view(self):
        
        self.client.login(username="testuser", password="password123")
        response = self.client.post(reverse("customers:address-create"), {"city": "gorgan", "state": "golestan", 
                                                                          "street": "edalat 97", "postal_code": "1234321"})
        self.assertEqual(response.status_code, 302) 


    def remove_from_wishlist(self):
        
        self.client.login(username="testuser", password="password123")
         
        product = Product.objects.create(
            name="Test Product",
            category = self.category,  
            brand = self.brand,
            price=1000,  
            stock=20,  
            description="Test Description"  
        )

        response = self.client.post(reverse("customers:wishlist-add", args=[product.id]))
        self.assertEqual(response.status_code, 302) 
        self.assertTrue(Wishlist.objects.filter(customer=self.customer, product=product).exists())

        response = self.client.post(reverse("customers:wishlist-remove", args=[product.id]))
        self.assertEqual(response.status_code, 302) 
        self.assertFalse(Wishlist.objects.filter(customer=self.customer, product=product).exists())