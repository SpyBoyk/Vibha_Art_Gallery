from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
from cart.cart import Cart
from accounts.models import Address
from .models import Order, OrderItem, Coupon
from .forms import OrderCreateForm
import uuid

def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        now = timezone.now()
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
            messages.success(request, f"Coupon '{code}' applied successfully!")
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, "Invalid or expired coupon code.")
    return redirect('cart_detail')

def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('shop')
        
    coupon = None
    discount = 0
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            discount = (coupon.discount / 100) * float(cart.get_total_price())
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    subtotal = float(cart.get_total_price())
    total = subtotal - discount

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            if coupon:
                order.coupon = coupon
                order.discount_amount = discount
            
            order.total_amount = total
            order.tracking_number = str(uuid.uuid4().hex[:10]).upper()
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                # Deduct stock
                product = item['product']
                product.stock = max(0, product.stock - item['quantity'])
                product.save()

            # Clear cart and coupon session
            cart.clear()
            request.session['coupon_id'] = None
            
            return redirect('order_success', order_id=order.id)
    else:
        # Prepopulate address if authenticated
        initial_data = {}
        if request.user.is_authenticated:
            default_address = Address.objects.filter(user=request.user, is_default=True).first()
            if not default_address:
                default_address = Address.objects.filter(user=request.user).first()
            
            if default_address:
                initial_data = {
                    'first_name': request.user.first_name or request.user.username,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    'phone': default_address.phone_number,
                    'address_line_1': default_address.address_line_1,
                    'address_line_2': default_address.address_line_2,
                    'city': default_address.city,
                    'state': default_address.state,
                    'postal_code': default_address.postal_code,
                    'country': default_address.country,
                }
        form = OrderCreateForm(initial=initial_data)

    context = {
        'cart': cart,
        'form': form,
        'coupon': coupon,
        'discount': discount,
        'total': total,
        'subtotal': subtotal,
    }
    return render(request, 'orders/checkout.html', context)

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/success.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})

def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/invoice_pdf.html', {'order': order})
    response = HttpResponse(html, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.html"'
    return response
