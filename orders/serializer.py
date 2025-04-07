from rest_framework import serializers
from orders.models import Order, OrderItem, DiscountByCode
from customers.models import Address
from products.models import Product

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class DiscountByCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountByCode
        fields = '__all__'




