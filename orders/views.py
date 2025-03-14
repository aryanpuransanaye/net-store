from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem
from products.models import Product

def customer_orders(request):
    
    customer = request.user.customer
    orders = Order.objects.filter(customer=customer)

    return render(request, 'orders/cart_detail.html', {'orders': orders})


def order_detail(request, order_id):
    
    order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
    
    return render(request, 'orders/order_detail.html', {'order': order})


def add_to_cart(request, product_id):
    
    if not request.user.is_authenticated:
        messages.error(request, "you need to login first.")
        return redirect('accounts:login')  

  
    product = get_object_or_404(Product, id=product_id)


    customer = request.user.customer
    order, created = Order.objects.get_or_create(
        customer=customer,
        status="Pending"
    )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 1, 'price': product.price}
    )

    if not created:
        
        order_item.quantity += 1
        order_item.save()

    
    order.total_price = sum(item.quantity * item.price for item in order.items.all())
    order.save()

    messages.success(request, f"{product.name} به سبد خرید شما اضافه شد.")
    
    return redirect('orders:order-detail', order_id=order.id) 