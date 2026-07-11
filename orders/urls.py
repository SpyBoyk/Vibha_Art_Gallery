from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.order_create, name='checkout'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('invoice/<int:order_id>/download/', views.download_invoice, name='download_invoice'),
]
