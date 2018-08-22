from django.contrib import admin
from django.urls import path,include
from .import views

from .views import (
    product_create_view,
    product_delete_view,
    product_list_view,
    product_detail_view,
    cart_add,
    cart_detail,
    cart_remove,
    order_create,
    search_list,
)

app_name="Product"
urlpatterns=[
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('create/',product_create_view,name='create'),
    path('<int:id>/delete/',product_delete_view,name='delete'),
    path('',product_list_view,name='list'),
    path('<int:id>',product_detail_view,name='product-detail'),
    path('cart/',cart_detail,name='cart-detail'),
    path('cart/add/<int:id>', cart_add,name='cart-add'),
    path('cart/remove/<int:id>', cart_remove,name='cart-remove'),
    path('order/create/',order_create,name='order_create'),
    path('search/',search_list,name='search'),
]