from django import forms
from .models import OrderItem

class Orderitemfroms(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product','quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }