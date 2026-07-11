from django import forms
from .models import ContactMessage, NewsletterSubscriber

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'subject': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-amber-500 focus:border-amber-500 bg-amber-50/50', 'rows': 5}),
        }

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'px-4 py-3 rounded-l-lg border-0 focus:ring-2 focus:ring-amber-500 bg-white/90 text-amber-900 placeholder-amber-700/60 w-full md:w-80',
                'placeholder': 'Your email address'
            }),
        }
