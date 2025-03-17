from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import DiscountByCode

@receiver(pre_save, sender=DiscountByCode)
def apply_discount_on_order(sender, instance, **kwargs):

    if instance.discount_code and instance.discount_code.is_valid():
        instance.discount_percentage = instance.discount_code.discount_percentage
    else:
        instance.discount_percentage = 0
