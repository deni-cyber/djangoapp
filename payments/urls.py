from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payment/', views.payment_callback, name='payment_callback'),
]