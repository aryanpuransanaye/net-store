from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from customers.models import Customer
from .forms import RegisterForm

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
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.is_staff = False
            user.is_superuser = False
            user.save()

           
            customer = Customer.objects.create(user=user)
            customer.phone = form.cleaned_data["phone"]
            customer.profile_picture = form.cleaned_data["profile_picture"]
            customer.save()

            login(request, user)
            messages.success(request, f"🎉 Welcome {user.first_name}! Your account has been created successfully.")
            
            next_url = request.GET.get("next")
            return redirect(next_url if next_url else "products:home")
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, "core/register.html", {"form": form})