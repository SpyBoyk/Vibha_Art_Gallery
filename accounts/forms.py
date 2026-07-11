from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Address

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'bio', 'profile_picture')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('full_name', 'phone_number', 'address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country', 'is_default')
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'address_line_1': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'address_line_2': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'state': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'postal_code': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'country': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-amber-600 focus:ring-amber-500 border-gray-300 rounded'}),
        }
