from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from users.models import Address
from .models import Order, OrderItem
from shipping.models import PickupPoint, Shipping
from products.models import Product
from cart.models import CartItem  # Import the CartItem model
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_daraja.mpesa.core import MpesaClient
from payments.models import Payment  # import your Payment model
from users.models import Profile

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_addresses = request.user.addresses.all()
    if not user_addresses.exists():
        return redirect('users:add_address')  # Redirect to address form if no address exists
    # Fetch user's cart items
    cart_items = CartItem.objects.filter(cart__user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Add items before checking out.")
        return redirect('cart_detail')  # Adjust to your cart view name

    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        selected_address_id = request.POST.get('address')
        selected_pickup_id = request.POST.get('pickup_point')
        
        # Fetch user's cart items and calculate total_amount
        cart_items = CartItem.objects.filter(cart__user=request.user)  # Adjust if your cart relationship is different
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Create the order
        order = Order.objects.create(
            user=request.user,
            address_id=selected_address_id if delivery_method == 'door_delivery' else None,
            pickup_point_id=selected_pickup_id if delivery_method == 'pickup' else None,
            total_amount=total_amount,
            status='Pending',  # Set the order status accordingly
        )

        # Create the shipping object (if needed)
        if delivery_method == 'door_delivery':
            shipping = Shipping.objects.create(
                order=order,
                provider="Provider Name",  # You can set a provider dynamically
                tracking_number="TRK123456",  # Optional tracking number
                estimated_delivery=order.created_at + timedelta(days=7),  # For example, 7 days from order creation
            )

        # Additional logic to save OrderItems (e.g. loop through cart items)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )

        return redirect('orders:order_summary', order_id=order.id)

    pickup_points = PickupPoint.objects.all()
    return render(request, 'orders/checkout.html', {
        'addresses': user_addresses,
        'pickup_points': pickup_points,
    })


def pay(phone, amount):
    import requests
    cl = MpesaClient()
    phone_number = phone
    amount = amount
    account_reference = 'ORDER'
    transaction_desc = 'Description' 
    callback_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return (response)


def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = order.items.all()
    profile = Profile.objects.get(user=request.user)
    phone_number = profile.phone

    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        amount = int(order.total_amount)

        # 1. Check if a Payment already exists for this Order
        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                'user': request.user,
                'phone_number': phone,
                'amount': amount,
                'status': 'Pending',
            }
        )

        if not created:
            # Optional: Update phone/amount if payment exists
            payment.phone_number = phone
            payment.amount = amount
            payment.status = 'Pending'
            payment.save()

        # 2. Try STK push
        try:
            response = pay(phone, amount)
            messages.info(request, f"Payment request sent to {phone}. Please check your phone.")
        except Exception as e:
            messages.error(request, f"Error initiating payment: {e}")

    return render(request, 'orders/order_summary.html', {
        'order': order,
        'order_items': order_items,
        'phone_number': phone_number, 
    })


def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/complete_order.html', {
            'order': order,
        })

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/user_orders.html', {'orders': orders})