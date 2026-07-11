from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop_view, name='shop'),
    path('categories/', views.categories_view, name='categories'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
]
