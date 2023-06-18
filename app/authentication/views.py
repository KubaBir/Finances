from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginUserForm, RegisterUserForm

# Create your views here.


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect("core:home")
        messages.error(request, "Error while registering.")
    form = RegisterUserForm()
    return render(request, 'authentication/register.html', context={'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, "Success!")
                return redirect('core:home')
        messages.error(request, 'Invalid credentials')
    form = LoginUserForm()
    return render(request, 'authentication/login.html', context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('core:home')
