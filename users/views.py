
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, AddressForm
from .models import Profile, Address


# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            login(request, user)
            return redirect('home')  # Redirect to home or dashboard after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# User Login View (optional if using Django's built-in LoginView)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or dashboard after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')  # Redirect to login page after logout



@login_required
def profile_view(request):
    addresses = Address.objects.filter(user=request.user)
    context = {
        'profile':Profile,
        'addresses': addresses,
    }
    return render(request, 'users/profile.html', context)


@login_required
def update_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('profile')
    else:
        profile_form = ProfileUpdateForm(instance=profile)

    addresses = Address.objects.filter(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    context = {
        'profile_form': profile_form,
    }
    return render(request, 'users/update_profile.html', context)

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')
    else:
        form = AddressForm()
    return render(request, 'users/add_address.html', {'form': form})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        return redirect('profile')
    return render(request, 'users/delete_address.html', {'address': address})
