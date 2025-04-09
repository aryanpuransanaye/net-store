from .models import Product

def products_count(request):
  
    count = Product.objects.count()
    return {'products_count': count}
