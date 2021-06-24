from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model

from . import models
from . import forms


def login_view(request):
    """Make a user login in the system. If already login redirect to the home"""
    if request.user.is_authenticated:
        return redirect('user:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            error = {'info': "Email Password doesn't match"}
            try:                                                           # Check If user exists
                _ = get_user_model().objects.get(email=email)
            except:
                error['info'] = "User with this email doesn't exists"
            return render(request, 'account/login.html', error)
        login(request, user)
        return redirect('user:home')
    return render(request, 'account/login.html')


def home(request):
    return render(request, 'home.html')


def logout_view(request):
    logout(request)
    return redirect('user:home')


def account_details(request):
    try:
        email = request.session['email']
        new_user = get_user_model().objects.get(email=email)
        is_new = True
    except:
        new_user = request.user
        is_new = False

    form = forms.UserProfileUpdateForm(request.POST or None, instance=new_user)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(is_new=is_new)
            if is_new:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['email']
                return redirect('user:home')

    context = {
        'profile': new_user,
        'form': form
    }

    return render(request, 'account/user_details.html', context)
