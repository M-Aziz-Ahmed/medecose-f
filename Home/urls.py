from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='layout'),
    path('about/',views.about),
    path('contact/', views.contact, name='contact'),
    path('features/', views.features),
    path('shop/', views.shop, name = 'shop'),
    path('product/<int:product_id>/', views.product_detail, name='product'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('confirm-order/', views.confirm_order, name='confirm_order'),
    path('thank-you/', views.thank_you, name='thank_you'),
]