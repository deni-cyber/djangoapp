# In products/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('products-listing/', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]
