from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from users.models import Address
from .models import Order, OrderItem
from shipping.models import PickupPoint, Shipping
from products.models import Product
from cart.models import CartItem  # Import the CartItem model
from datetime import timedelta

'''def checkout(request):
    # Redirect to login if user is not authenticated
    if not request.user.is_authenticated:
        return redirect('login')

    # Fetch user's addresses
    user_addresses = request.user.addresses.all()
    if not user_addresses.exists():
        return redirect('users:add_address')  # Redirect to address form if no address exists

    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        selected_address_id = request.POST.get('address')
        selected_pickup_id = request.POST.get('pickup_point')

        # Fetch user's cart items and calculate total_amount
        cart_items = CartItem.objects.filter(cart__user=request.user)  # Adjust if your cart relationship is different
        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        with transaction.atomic():
            # Create the order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount,
                status='Pending'
            )

            # Add order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Create Shipping based on delivery method
            if delivery_method == 'door_delivery':
                shipping = Shipping.objects.create(
                    order=order,
                    delivery_type='door_delivery',
                    address_id=selected_address_id
                )
            elif delivery_method == 'pickup':
                shipping = Shipping.objects.create(
                    order=order,
                    delivery_type='pickup_point',
                    pickup_point_id=selected_pickup_id
                )

        return redirect('orders:order_summary', order_id=order.id)

    # Get all pickup points
    pickup_points = PickupPoint.objects.all()

    return render(request, 'orders/checkout.html', {
        'addresses': user_addresses,
        'pickup_points': pickup_points
    })
'''

'''def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_addresses = request.user.addresses.all()
    if not user_addresses.exists():
        return redirect('users:add_address')  # Redirect to address form if no address exists

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
            # Importing here to avoid circular import
            from orders.models import Order  # Local import to avoid circular import
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
'''


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_addresses = request.user.addresses.all()
    if not user_addresses.exists():
        return redirect('users:add_address')  # Redirect to address form if no address exists

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

def order_summary(request, order_id):
    # Fetch the order based on the order_id
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Fetch the order items associated with this order
    order_items = order.items.all()

    return render(request, 'orders/order_summary.html', {
        'order': order,
        'order_items': order_items,
    })


def complete_order(request, order_id):
    ##### i shall use this view to initiate the payment gateway. ######
    
    # Fetch the order based on order_id
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Optionally, create shipping info here (if using Shipping model)
    # Shipping.objects.create(order=order, provider='Your provider', tracking_number='Your tracking number', estimated_delivery='Estimated date')

    # Redirect to order summary after completing the order
    return render(request, 'orders/complete_order.html', {
            'order': order,
        })