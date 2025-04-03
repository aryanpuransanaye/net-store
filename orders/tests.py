from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from decimal import Decimal
from products.models import Product, Category, Brand
from customers.models import Customer
from orders.models import Order, OrderItem, DiscountByCode
import datetime
from django.utils import timezone

User = get_user_model()

class OrderTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.customer = Customer.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(name="Electronics")
        self.brand = Brand.objects.create(name="BrandX")

        self.product = Product.objects.create(
            name = "Test Product",
            category = self.category,
            brand = self.brand,
            price = Decimal('100.00'),
            final_price = Decimal('120.00'),
            stock = 10,
            description = "Test Description"
        )     

        self.order = Order.objects.create(customer = self.customer, status = 'Pending', total_price = Decimal('0.00'))
        
        self.discount = DiscountByCode.objects.create(
            discount_code = 'TEST10',
            discount_percentage = 10,
            start_date = timezone.now() - datetime.timedelta(days=1),
            end_date = timezone.now() + datetime.timedelta(days=1),
            max_usage = 5,
            used_count = 0
        )
    
    def test_add_to_cart(self):
        url = reverse('orders:add-to-cart', args = [self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(OrderItem.objects.count(), 1)
        
    def test_remove_order(self):
        order = Order.objects.create(customer=self.customer, status='Pending')
        url = reverse('orders:remove-order', args=[order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(Order.objects.filter(id=order.id).exists())
        
    def test_remove_order_item(self):

        order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1, price=self.product.price)
        url = reverse('orders:remove-order-item', args=[self.order.id, order_item.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertFalse(OrderItem.objects.filter(id=order_item.id).exists())
        
    def test_apply_discount(self):
        self.order.total_price = Decimal('200.00')
        self.order.save()
        
        url = reverse('orders:apply-discount', args=[self.order.id])
        response = self.client.post(url, {'discount_code': 'TEST10'})
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        
        self.order.refresh_from_db()
        expected_discount = Decimal('200.00') * Decimal('0.10')
        expected_final_price = Decimal('200.00') - expected_discount
        self.assertEqual(self.order.final_price, expected_final_price)