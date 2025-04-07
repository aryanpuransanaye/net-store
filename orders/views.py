from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from .models import Order, OrderItem, DiscountByCode
from products.models import Product
from decimal import Decimal
from customers.models import Address
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializer import OrderSerializer, AddressSerializer, OrderItemSerializer

class CustomerOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id=None):
        customer = request.user.customer

        if order_id:
            order = get_object_or_404(Order, id=order_id, customer=customer)
            address = get_object_or_404(Address, customer=customer, is_active=True)
            orderitem_data = OrderSerializer(order).data
            address_data = AddressSerializer(address).data

            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                return render(request, 'orders/order_detail.html', {'order': order, 'address': address})
            else:
                return Response({'orders': orderitem_data, 'address': address_data})
            
        orders = Order.objects.filter(customer=customer)
        
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return render(request, 'orders/cart_detail.html', {'orders': orders})
        else:
            orders_data = OrderSerializer(orders, many=True).data
            return Response({'orders': orders_data})

    
class AddToCartView(APIView):

    def post(self, request, product_id):
    
        if not request.user.is_authenticated:
            return redirect('core:login')

        customer = request.user.customer

        addresses = Address.objects.filter(customer=customer)
        if not addresses:
            messages.warning(request, 'You dont have any Address, Please creat your Address.')
            return redirect('customers:address-create')

        product = get_object_or_404(Product, id=product_id)

        order, created = Order.objects.get_or_create(customer=customer, status="Pending")

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

        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return redirect('products:product-detail', product_id = product.id)
        else:
            return Response({
                "message": f"{product.name} has been added to the cart.",
                "order": OrderSerializer(order).data,
                "order_item": OrderItemSerializer(order_item).data,})


class RemoveOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
    
        order = get_object_or_404(Order, id=order_id, customer=request.user.customer, status="Pending")

        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            product = item.product
            product.stock += item.quantity 
            product.save()

        order.delete()
    
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            return redirect('orders:orders')
        else:
            order_items_data = OrderItemSerializer(order_items, many=True).data
            return Response({
            "message": "Order has been successfully removed.",
            "order_items": order_items_data})
            

class RemoveOrderItemView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, order_id, item_id):
       
        order = get_object_or_404(Order, id=order_id, customer=request.user.customer, status="Pending")
        item = get_object_or_404(OrderItem, id=item_id, order=order)

        product = item.product

        if item.quantity > 1:
            item.quantity -= 1
            item.save()

            product.stock += 1
            product.save()

            message = f"One {item.product.name} has been removed from your Cart."
        elif item.quantity == 1:
            item.delete()
            message = f"{item.product.name} has been deleted successfully."

        if not order.items.exists():
            order.delete()
            message += " Your order has been completely removed as it had no items."
        else:
            order.total_price = order.update_total_price()
            order.save()


        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            previous_url = request.META.get('HTTP_REFERER', '/')
            return redirect(previous_url)
        else:
            remove_order_items_data = OrderItemSerializer(order, many=True).data
            return Response({
            "message": "Order has been successfully removed.",
            "order_items": remove_order_items_data})
        

class ApplyDiscountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
       
        discount_code = request.data.get("discount_code", "").strip()

        order = get_object_or_404(Order, id=order_id, customer=request.user.customer)

        try:
            discount = DiscountByCode.objects.filter(discount_code=discount_code).first()

            if discount: 
                discount_percentage = Decimal(discount.discount_percentage) / Decimal(100)
                discount_amount = order.total_price * discount_percentage

                order.final_price = order.total_price - discount_amount
                order.discount_percentage = discount.discount_percentage
                order.discount_code = discount
                discount.used_count += 1
                order.save()
                discount.save()

                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    return redirect('orders:orders')
                else:
                    order_data = OrderSerializer(order).data
                    return Response({
                        "message": "Discount applied successfully.",
                        "order": order_data})
            else:
                if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                    messages.error(request, 'Discount code is not valid or expired.')
                    return redirect('orders:order-detail', order_id=order.id)
                else:
                    return Response({"error": "Discount code is not valid or expired."})
                
        except DiscountByCode.DoesNotExist:
            if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                messages.error(request, 'Discount code does not exist.')
                return redirect('orders:order-detail', order_id=order.id)
            else:
                return Response({"error": "Discount code does not exist."})