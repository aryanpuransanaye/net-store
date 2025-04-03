from django.test import TestCase, Client
from django.contrib.auth.models import User
from customers.models import Customer
from django.urls import reverse

class CoreViewsTest(TestCase):
    def setUp(self):
     
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.client = Client()

    def test_login_view(self):
       
        response = self.client.post(reverse("core:login"), {
            "username": "testuser",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 302) 
        self.assertRedirects(response, reverse("products:home"))

    def test_logout_view(self):
        
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("core:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("products:home"))

    def test_register_view(self):
        
        with open("C:/Users/aryan/OneDrive/Pictures/photo_2025-01-01_14-58-11.jpg", 'rb') as img:

            response = self.client.post(reverse("core:register"), {
            "username": "newuser",
            "email": "uniqueemail@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
            "first_name": "New",
            "last_name": "User",
            "phone": "09123456789", 
            "profile_picture": img
        })
            
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("products:home"))
        self.assertTrue(Customer.objects.filter(user__username="newuser").exists())