from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Address, Wishlist
from .forms import AddressForm
from products.models import Product


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
            return redirect('address-list')
    else:
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})


def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    
    if request.user != address.customer.user:
        messages.error(request, "شما اجازه ویرایش این آدرس را ندارید.")
        return redirect('home')  

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "آدرس با موفقیت ویرایش شد.")
            return redirect('address_list')  
    else:
        form = AddressForm(instance=address)

    return render(request, 'edit_address.html', {'form': form})


def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    if request.user != address.customer.user:
        messages.error(request, "شما اجازه حذف این آدرس را ندارید.")
        return redirect('home') 

    if request.method == 'POST':
        address.delete()
        messages.success(request, "آدرس با موفقیت حذف شد.")
        return redirect('address_list') 

    return render(request, 'delete_address.html', {'address': address})


def wishlist_list(request):
    customer = request.user.customer  
    wishlist = Wishlist.objects.get(customer=customer)
    return render(request, 'wishlist_list.html', {'wishlist': wishlist})


def wishlist_add(request, product_id):
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(customer=customer)
    wishlist.product.add(product)
    return redirect('wishlist-list')
