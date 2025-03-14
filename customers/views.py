from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Address, Wishlist
from .forms import AddressForm
from products.models import Product
from orders.models import Order, OrderItem


def address_list(request):
    customer = request.user.customer
    addresses = Address.objects.filter(customer = customer)
    return render(request, 'customers/address_list.html', {'addresses': addresses})


def address_create(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = request.user.customer  
            address.save()
            return redirect('customers:address-list')
    else:
        form = AddressForm()
    return render(request, 'customers/address_create.html', {'form': form})


def edit_address(request, address_id):

    address = get_object_or_404(Address, id=address_id, customer=request.user.customer)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Your address has been updated successfully.")
            return redirect('customers:address-list')  
    else:
        form = AddressForm(instance=address)

    return render(request, 'customers/edit_address.html', {'form': form})


def delete_address(request, address_id):

    address = get_object_or_404(Address, id=address_id, customer=request.user.customer)
    address.delete()  
    messages.success(request, "Your address has been deleted successfully.")  

    return redirect('customers:address-list')  


def wishlist_list(request):
    
    customer = request.user.customer

    try: 
        wishlist = Wishlist.objects.get(customer=customer)
    except Wishlist.DoesNotExist:
        wishlist = None

    return render(request, 'customers/wishlist_list.html', {'wishlist': wishlist})


def remove_from_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.get(customer=request.user.customer)
    
    wishlist.product.remove(product)
    messages.success(request, f"✅ {product.name} removed from your wishlist.")
    
    return redirect('customers:wishlist-list')


def wishlist_add(request, product_id):

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(customer=customer)
    wishlist.product.add(product)
    return redirect('customers:wishlist-list')


def product_select(request):

    all_products = Product.objects.all()
    return render(request, 'customers/product_select.html', {'products': all_products})

