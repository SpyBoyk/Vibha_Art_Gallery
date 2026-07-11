from django import forms
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ('rating', 'title', 'content')
        widgets = {
            'rating': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50', 'placeholder': 'Summarize your experience'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50', 'rows': 4, 'placeholder': 'Write your feedback here...'}),
        }
