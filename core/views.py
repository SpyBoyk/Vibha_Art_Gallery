from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, Category, Banner, ProductReview
from .models import BlogPost, ContactMessage
from .forms import ContactMessageForm, NewsletterForm

def home_view(request):
    banners = Banner.objects.filter(is_active=True).order_by('order')
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    trending_products = Product.objects.filter(is_active=True, is_trending=True)[:8]
    best_sellers = Product.objects.filter(is_active=True, is_best_seller=True)[:8]
    categories = Category.objects.all()[:6]
    blogs = BlogPost.objects.all().order_by('-created_at')[:3]
    reviews = ProductReview.objects.filter(rating__gte=4).order_by('-created_at')[:5]

    newsletter_form = NewsletterForm()

    context = {
        'banners': banners,
        'featured_products': featured_products,
        'trending_products': trending_products,
        'best_sellers': best_sellers,
        'categories': categories,
        'blogs': blogs,
        'reviews': reviews,
        'newsletter_form': newsletter_form,
    }
    return render(request, 'core/home.html', context)

def about_view(request):
    return render(request, 'core/about.html')

from handcrafted_mall.email_helper import send_submission_email

def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            instance = form.save()
            send_submission_email("Contact Inquiry Form Submission", {
                'Name': instance.name,
                'Email': instance.email,
                'Subject': instance.subject,
                'Message': instance.message,
            })
            messages.success(request, "Your message has been sent successfully. We will get back to you shortly!")
            return redirect('contact')
    else:
        form = ContactMessageForm()
    return render(request, 'core/contact.html', {'form': form})

def faq_view(request):
    return render(request, 'core/faq.html')

def privacy_view(request):
    return render(request, 'core/privacy.html')

def terms_view(request):
    return render(request, 'core/terms.html')

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            instance = form.save()
            send_submission_email("Newsletter Subscription", {
                'Email': instance.email,
            })
            messages.success(request, "Thank you for subscribing to our newsletter!")
        else:
            messages.error(request, "This email is already subscribed or invalid.")
    return redirect('home')

def blog_list(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'core/blog_list.html', {'blogs': blogs})

def blog_detail(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    recent_blogs = BlogPost.objects.exclude(id=blog.id).order_by('-created_at')[:3]
    return render(request, 'core/blog_detail.html', {'blog': blog, 'recent_blogs': recent_blogs})
