from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from customers.models import Customer, Address
from products.models import Product, Category, Brand
from decimal import Decimal
from django.utils import timezone
import datetime
from orders.models import Order, OrderItem, DiscountByCode

class OrderTestCase(APITestCase):

    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')
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

        self.address = Address.objects.create(customer=self.customer, is_active=True, city='City', street='Street')     

        self.order = Order.objects.create(customer = self.customer, status = 'Pending', total_price = Decimal('0.00'), address = self.address)
        
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1, price=self.product.price)

        self.discount = DiscountByCode.objects.create(
            discount_code = 'TEST10',
            discount_percentage = 10,
            start_date = timezone.now() - datetime.timedelta(days=1),
            end_date = timezone.now() + datetime.timedelta(days=1),
            max_usage = 5,
            used_count = 0
        )
    def test_customer_order_list_api(self):

        url = reverse('orders:orders') 
        response = self.client.get(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('orders', response.data)

    def test_customer_order_detail_html(self):

        url = reverse('orders:order-detail', args=[self.order.id])
        response = self.client.get(url, HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.product.name)

    def test_add_to_cart_api(self):

        url = reverse('orders:add-to-cart', args=[self.product.id])
        response = self.client.post(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_add_to_cart_html(self):

        url = reverse('orders:add-to-cart', args=[self.product.id])
        response = self.client.post(url, HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_remove_order_api(self):

        url = reverse('orders:remove-order', args=[self.order.id])
        response = self.client.post(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Order.objects.filter(id=self.order.id).exists())

    def test_remove_order_html(self):

        url = reverse('orders:remove-order', args=[self.order.id])
        response = self.client.post(url, HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    def test_remove_order_item_api(self):

        url = reverse('orders:remove-order-item', args=[self.order.id, self.order_item.id])
        response = self.client.post(url, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_order_item_html(self):

        url = reverse('orders:remove-order-item', args=[self.order.id, self.order_item.id])
        response = self.client.post(url, HTTP_ACCEPT='text/html')
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/'))

    def test_apply_discount_api(self):

        url = reverse('orders:apply-discount', args=[self.order.id])
        response = self.client.post(url, {'discount_code': 'TEST10'}, HTTP_ACCEPT='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Discount applied successfully.')

    def test_apply_discount_html_invalid(self):

        url = reverse('orders:apply-discount', args=[self.order.id])
        response = self.client.post(url, {'discount_code': 'INVALID'}, HTTP_ACCEPT='text/html')
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)