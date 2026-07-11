from django.contrib import admin
from .models import Coupon, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'total_amount', 'payment_method', 'status', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'tracking_number')
    inlines = [OrderItemInline]

admin.site.register(Coupon)
admin.site.register(Order, OrderAdmin)
