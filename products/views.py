from django.shortcuts import render, get_object_or_404
from .models import Product, Brand, Category, Tag

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