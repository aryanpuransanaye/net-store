# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.utils import timezone
# from decimal import Decimal
# from .models import Discount
# from customers.models import Customer

# @receiver(post_save, sender=Discount)
# @receiver(post_delete, sender=Discount)
# def update_product_price(sender, instance, **kwargs):

#     product = instance.product

#     valid_discounts = Discount.objects.filter(
#         product=product,
#         start_date__lte=timezone.now(),
#         end_date__gte=timezone.now()
#     )
    
#     if valid_discounts.exists():
#         discount_amount = Decimal(str(instance.discount_percentage)) / Decimal('100')
#         product.final_price = product.price * (Decimal('1') - discount_amount)
#         product.discount_percentage = instance.discount_percentage
#     else:
#         product.final_price = product.price
#         product.discount_percentage = 0  

#     product.save()  
