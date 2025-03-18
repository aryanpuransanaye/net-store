from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from customers.models import Customer

def login_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('products:home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


def logout_view(request):

    logout(request)
    messages.success(request, "You have logged out successfully!")

    return redirect('products:home')


def register_view(request):

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "❌ Passwords do not match! Please try again.")
            return redirect("auth:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "❌ This username is already taken!")
            return redirect("core:register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "❌ An account with this email already exists!")
            return redirect("auth:register")

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = False
        user.is_superuser = False
        user.save()

        customer = Customer.objects.create(user=user)
        customer.save()

        login(request, user)
        messages.success(request, f"🎉 Welcome {user.first_name}! Your account has been created successfully.")

        next_url = request.GET.get("next")
        if next_url:
            return HttpResponseRedirect(next_url)
        return redirect("products:home")  

    return render(request, "core/register.html")