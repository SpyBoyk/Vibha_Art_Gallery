from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, ProductImage, ProductReview
from .forms import ProductReviewForm

def shop_view(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.all()

    # Search query
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(sku__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Availability filter
    in_stock = request.GET.get('in_stock')
    if in_stock == '1':
        products = products.filter(stock__gt=0)

    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'popularity':
        products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')

    # Pagination can be done via django standard templates but simple list works perfectly.
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
    }
    return render(request, 'products/shop.html', context)

def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'products/categories.html', {'categories': categories})

def get_humanized_description(product):
    desc = product.description or ""
    color = ""
    features = ""
    best_for = ""
    moq = ""
    
    if "Color:" in desc:
        parts = desc.split("Color:")
        color = parts[1].split(".")[0].strip()
    
    if "Features:" in desc:
        parts = desc.split("Features:")
        features = parts[1].split(".")[0].strip().replace(" | ", ", ")
    
    if "Best For:" in desc:
        parts = desc.split("Best For:")
        best_for = parts[1].split(".")[0].strip().replace(" + ", " and ")
        
    if "MOQ:" in desc:
        parts = desc.split("MOQ:")
        moq = parts[1].split(".")[0].strip()
        
    intro = desc.split(".")[0] if desc else "A premium presentation display solution"
    human_desc = f"{intro}. "
    
    if color:
        human_desc += f"Draped in a luxury {color.lower()} finish, this display accessory offers an elegant background contrast that accentuates the details and beauty of your precious jewelry items. "
    
    if features:
        human_desc += f"It has been meticulously crafted with showroom counters and boutique displays in mind, incorporating features like {features.lower()} to ensure ease of styling and secure presentation. "
    
    if best_for:
        human_desc += f"This display solution is highly recommended and best suited for {best_for.lower()}, helping elevate visual merchandising setups and grab shoppers' attention. "
        
    if moq:
        human_desc += f"This product is available for wholesale and retail ordering with a minimum order quantity of {moq}."
    else:
        human_desc += "Perfect for boutique setups and luxury retail showrooms looking to enhance their counter space and customer presentations."
        
    return human_desc

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.images.all()
    reviews = product.reviews.all().order_by('-created_at')
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]

    # Dynamic human-friendly description
    product.human_description = get_humanized_description(product)

    # Handle review submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to submit a review.")
            return redirect('login')
        
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted!")
            return redirect('product_detail', slug=product.slug)
    else:
        form = ProductReviewForm()

    context = {
        'product': product,
        'images': images,
        'reviews': reviews,
        'related_products': related_products,
        'review_form': form,
    }
    return render(request, 'products/product_detail.html', context)
