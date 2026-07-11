from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'address_line_1', 'address_line_2', 'city', 
            'state', 'postal_code', 'country', 'payment_method'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'address_line_1': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'address_line_2': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'state': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'payment_method': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
        }
