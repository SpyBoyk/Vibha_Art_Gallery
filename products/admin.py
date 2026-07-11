from django.contrib import admin
from .models import Category, Product, ProductImage, ProductReview, Banner

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_price', 'stock', 'sku', 'is_featured', 'is_trending', 'is_best_seller', 'is_active')
    list_filter = ('is_featured', 'is_trending', 'is_best_seller', 'is_active', 'category')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)
admin.site.register(Banner)
