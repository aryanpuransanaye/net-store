from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem, DiscountByCode
from products.models import Product
from decimal import Decimal
from customers.models import Address
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class CustomerOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id=None):
        customer = request.user.customer
        if order_id:
            order = get_object_or_404(Order, id=order_id, customer=customer)
            address = get_object_or_404(Address, customer=customer, is_active=True)
            return render(request, 'orders/order_detail.html', {'order': order, 'address': address})
        
        orders = Order.objects.filter(customer=customer)
        return render(request, 'orders/cart_detail.html', {'orders': orders})
    
class AddToCartView(APIView):
    
    def post(self, request, product_id):

        if not request.user.is_authenticated:
            return redirect('core:login')
        
        customer = request.user.customer

        addresses = Address.objects.filter(customer = customer)
        if not addresses:
            messages.warning(request, 'You dont have any Address, Please creat your Address.')
            return redirect('customers:address-create')
        
        product = get_object_or_404(Product, id=product_id)
    
        order, created = Order.objects.get_or_create(customer=customer, status = "Pending")

        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={'quantity': 1, 'price': product.final_price}
        )

        if not created:
            order_item.quantity += 1
            product.stock -= 1
            product.save()
            order_item.save()

        order.total_price = order.update_total_price()
        
        order.save()

        messages.success(request, f"{product.name} Added to cart")

        return redirect('products:product-detail', product_id = product.id)


class RemoveOrderView(APIView):

    def post(self, request, order_id):

        order = get_object_or_404(Order, id=order_id, customer=request.user.customer, status = "Pending")
        order_item = OrderItem.objects.filter(order = order)

        for item in order_item:
            product = item.product
            product.stock += item.quantity
            product.save()

        order.delete()

        messages.success(request, "Your order has been completely removed as it had no items.")
        return redirect('orders:orders')


class RemoveOrderItemView(APIView):

    def post(self, request, order_id, item_id):

        order = get_object_or_404(Order, id=order_id, customer=request.user.customer, status = "Pending")
        item = get_object_or_404(OrderItem, id=item_id, order=order)

        product = item.product
        
        if item.quantity > 1:
            item.quantity -= 1
            item.save()

            product.stock += 1
            product.save()

            messages.success(request, f"One {item.product.name} has been removed from your Cart.")

        elif item.quantity == 1:
            item.delete()
            messages.success(request, f"{item.product.name} has been deleted successfully.")
        
        if order.items.count() == 0:
            order.delete()
            messages.success(request, "Your order has been completely removed as it had no items.")
        else:
            order.total_price = order.update_total_price()
            order.save()

        return redirect('products:product-detail', product_id=item.product.id)


class ApplyDiscountView(APIView):

    def post(self, request, order_id):

        discount_code = request.POST.get("discount_code", "").strip()
        if not discount_code:
            return redirect('orders:order-detail', order_id=order_id)

        order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
        try:
            discount = get_object_or_404(DiscountByCode, discount_code = discount_code)

            if discount.is_valid():
                discount_percentage = Decimal(discount.discount_percentage) / Decimal(100)
                discount_amount = order.total_price * discount_percentage

                order.final_price = order.total_price - discount_amount
                order.discount_percentage = discount.discount_percentage
                order.discount_code = discount
                discount.used_count += 1
                order.save()
                discount.save()

        except DiscountByCode.DoesNotExist:
            pass

        return redirect('orders:order-detail', order_id=order.id)
