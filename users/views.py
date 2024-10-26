
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from django.contrib import messages

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
