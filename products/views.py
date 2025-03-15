from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, Brand, Category, Tag, Review
from .forms import ReviewForms
from customers.models import Customer
from django.db.models import Avg


def home(request):

    products = Product.objects.all()
    brands = Brand.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    return render(request, 'products/home.html', {
        'products': products,
        'brands': brands,
        'categories': categories,
        'tags': tags
    })


def product_detail(request, product_id):

    product = get_object_or_404(Product, id = product_id)
    return render(request, 'products/product_detail.html', {'product': product})

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


def product_by_brand(request, brand_id):

    brand = get_object_or_404(Brand, id = brand_id) 
    products = Product.objects.filter(brand=brand)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'products/home.html', {
        'products': products,
        'brands': brands,
        'categories': categories,
        'tags': tags 
    })


def product_by_category(request, category_id):
    
    category = get_object_or_404(Category, id = category_id)
    products = Product.objects.filter(category=category)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'products/home.html', {
        'products': products,
        'brands': brands,
        'categories': categories,
        'tags': tags
    })

def product_by_tag(request, tag_id):

    tag = get_object_or_404(Tag, id = tag_id)
    products = Product.objects.filter(tag=tag)
    brands = Brand.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'products/home.html', {
        'products': products,
        'brands': brands,
        'categories': categories,
        'tags': tags
    })


def sort_product(request):


    products = Product.objects.all()

    price_filter = request.GET.get('price')
    rating_filter = request.GET.get('rating')

    if price_filter == 'asc':
        products = products.order_by('price')  
    elif price_filter == 'desc':
        products = products.order_by('-price') 

    if rating_filter == 'asc':
        products = products.annotate(avg_rating=Avg('review__rating')).order_by('avg_rating') 
    elif rating_filter == 'desc':
        products = products.annotate(avg_rating=Avg('review__rating')).order_by('-avg_rating') 

    return render(request, 'products/home.html', {
        'products': products,
        'price_filter': price_filter,
        'rating_filter': rating_filter,
    })
