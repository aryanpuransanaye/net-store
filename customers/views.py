from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Address, Wishlist, Customer
from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from products.models import Product


@login_required
def customer_profile(request):

    user = request.user
    
    try:
        customer = Customer.objects.get(user=user)
        phone_number = customer.phone
        status = customer.status
        profile_picture = customer.profile_picture
    except Customer.DoesNotExist:
       
        phone_number = None
        status = 'Inactive'
        profile_picture = None
    
    context = {
        'user': user,
        'phone_number': phone_number,
        'profile_picture': profile_picture,
        'status': status,
    }
    
    return render(request, 'customers/customer_profile.html', context)

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

def set_active_address(request, address_id):

    address = get_object_or_404(Address, id = address_id, customer = request.user.customer)

    Address.objects.filter(customer = request.user.customer, is_active = True).update(is_active = False)

    address.is_active = True
    address.save()

    messages.success(request, "Your active address has been updated successfully!")
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

@login_required
def wishlist_add(request, product_id):

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(customer=customer)
    wishlist.product.add(product)

    messages.success(request, f"✅ '{product.name}' has been added to your wishlist!")

    return redirect('customers:wishlist-list')


def product_select(request):

    all_products = Product.objects.all()
    return render(request, 'customers/product_select.html', {'products': all_products})

