from .forms import ReviewForms
from django.db.models import Avg, Q
from django.contrib import messages
from customers.models import Customer
from django.utils import timezone
from decimal import Decimal
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, Brand, Category, Review, Discount
from orders.models import OrderItem, Order
from django.contrib.auth.decorators import login_required


def home(request):

    products_list = Product.objects.all().order_by('id')
    
    categories = Category.objects.all()
    brands = Brand.objects.all()

    selected_category = request.GET.get('category')
    selected_brand = request.GET.get('brand')
    price_filter = request.GET.get('price')
    rating_filter = request.GET.get('rating')

    if selected_category and selected_category.isdigit():
        products_list = products_list.filter(category_id=selected_category)

    if selected_brand and selected_brand.isdigit():
        products_list = products_list.filter(brand_id=selected_brand)

    if price_filter == 'asc':
        products_list = products_list.order_by('price')
    elif price_filter == 'desc':
        products_list = products_list.order_by('-price')

    if rating_filter in ['asc', 'desc']:
        products_list = products_list.annotate(avg_rating=Avg('review__rating'))
        if rating_filter == 'asc':
            products_list = products_list.order_by('avg_rating')
        else:
            products_list = products_list.order_by('-avg_rating')

    updated_products = []
    for product in products_list:
        valid_discounts = Discount.objects.filter(
            product=product,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )

        if valid_discounts.exists():
            latest_discount = valid_discounts.order_by('-start_date').first()
            discount_amount = Decimal(str(latest_discount.discount_percentage)) / Decimal('100')
            product.final_price = (product.price * (Decimal('1') - discount_amount)).quantize(Decimal('0.01'))
            product.discount_percentage = latest_discount.discount_percentage
        else:
            product.final_price = product.price
            product.discount_percentage = 0

        updated_products.append(product)
    Product.objects.bulk_update(updated_products, ['final_price', 'discount_percentage'])


    paginator = Paginator(products_list, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/home.html', {
        'products_list': products_list,
        'page_obj': page_obj,
        'categories': categories,
        'brands': brands,
        'selected_category': selected_category,
        'selected_brand': selected_brand,
        'price_filter': price_filter,
        'rating_filter': rating_filter,
    })


def search_product(request):
    
    query = request.GET.get('q', '')
    products = Product.objects.all()
    
    if query:
         products = products.filter(
            Q(name__icontains=query) |
            Q(tag__name__icontains=query) |
            Q(brand__name__icontains=query) |  
            Q(category__name__icontains=query) 
        ).distinct()
    
    return render(request, 'products/search_results.html', {
        'products': products, 'query': query
        })


def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        order = Order.objects.filter(customer=request.user.customer, status='Pending').first()
        
        order_item = OrderItem.objects.filter(product=product, order=order).first()

        return render(request, 'products/product_detail.html', {
            'product': product,
            'order_item': order_item,
            'order': order
        })
    
    return render(request, 'products/product_detail.html', {
            'product': product,
            'order_item': None,
            'order': None
        })


@login_required
def product_review(request, product_id):

    product = get_object_or_404(Product, id = product_id)
    reviews = Review.objects.filter(product = product)

    return render(request, 'products/review_list.html', {'product': product, 'reviews': reviews})


@login_required
def add_product_review(request, product_id):
    
    product = get_object_or_404(Product, id = product_id)
    customer = get_object_or_404(Customer, user=request.user)

    if request.method == 'POST':
        form = ReviewForms(request.POST)
        if form.is_valid():
            review = form.save(commit = False)
            review.product = product
            review.user = customer
            review.save()
            messages.success(request, "Your review has been added successfully!")
            return redirect('products:product-detail', product_id=product.id)
        else:
            messages.error(request, "There was an error submitting your review.")
    else:
        form = ReviewForms()

    return render(request, "products/add_review.html", {"form": form, "product": product})


