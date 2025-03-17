from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, OrderItem, DiscountByCode
from products.models import Product
from django.utils import timezone
from decimal import Decimal

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
        defaults={'quantity': 1, 'price': product.final_price}
    )

    if not created:
        
        order_item.quantity += 1
        order_item.save()

    
    order.total_price = order.update_total_price()

    messages.success(request, f"{product.name} Added to cart")
    
    return redirect('orders:order-detail', order_id=order.id) 


def remove_order(request, order_id):
    
    order = get_object_or_404(Order, id=order_id)

    order.delete()
    
    messages.success(request, "Your order has been deleted successfully.")
    
    return redirect('orders:customer-orders')

def remove_order_item(request, order_id, item_id):

    order = get_object_or_404(Order, id=order_id)
    item = get_object_or_404(OrderItem, id=item_id, order=order)
    
    item.delete()
    messages.success(request, f"Item '{item.product.name}' has been removed from your order.")
    

    if order.items.count() == 0:
        order.delete()
        messages.success(request, "Your order has been completely removed as it had no items.")
        return redirect('orders:customer-orders')
    else:
        order.total_price = order.update_total_price()
        return redirect('orders:order-detail', order_id=order.id)  


def apply_discount(request, order_id):

    if request.method == "POST":
        discount_code = request.POST.get("discount_code", "").strip() 
        order = get_object_or_404(Order, id=order_id)  
        
        try:
            discount = DiscountByCode.objects.get(discount_code=discount_code)

            if discount.is_valid():
                
                discount_percentage = Decimal(discount.discount_percentage) / Decimal(100)
                discount_amount = order.total_price * discount_percentage
             
                order.total_price -= discount_amount
                order.discount_percentage = discount.discount_percentage
                order.discount_code = discount  
                order.save() 

                messages.success(request, f"✅ Discount applied successfully! You saved ${discount_amount:.2f}.")
            else:
                messages.error(request, "❌ This discount code has expired or is invalid.")
                    
        except DiscountByCode.DoesNotExist:
            messages.error(request, "❌ Invalid discount code.")

    return redirect("orders:order-detail", order_id=order.id)