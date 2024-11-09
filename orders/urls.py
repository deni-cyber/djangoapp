from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('complete/<int:order_id>/', views.complete_order, name='complete_order'),
]
