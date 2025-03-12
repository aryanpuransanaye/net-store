from django.shortcuts import render, redirect, get_object_or_404
from .models import Order
from .forms import Orderitemfroms

def customer_order_list(request):

    customer = request.user.customer
    orders = Order.objects.filter(customer = customer)
    
    return render(request, 'orders/customer_order_list.html', {'orders': orders})

def add_order_item(request, id):

    order = get_object_or_404(Order, id=id)

    if request.method == 'POST':
        form = Orderitemfroms(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            return redirect('order-list')
        else:
            form = Orderitemfroms(request.POST)

    return render(request, 'orders/add_order_item.html', {'form': form})

def delete_order(request, id):

    order = get_object_or_404(Order, id=id, customer = request.user.customer)

    if order.status == 'pending':
        order.delete()

    return redirect('customer_order-list')

def order_detail(request, id):

    order = get_object_or_404(Order, id=id, customer = request.user.customer)
    
    return render(request, 'orders/order_detail.html', {'order': order})
