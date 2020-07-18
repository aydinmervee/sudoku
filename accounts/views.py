from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, RegisterForm


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        # Bu username ve password a sahip veritabanindaki kullaniciyi alir,
        user = authenticate(username=username, password=password)
        # Yukarda aldigi user ile login olmayi dener.
        login(request, user)
        return redirect('index')
    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password1')
        # Set password kullanilma sebebi, kisinin sifresinin
        # hashli (sifreli) bir sekilde gosterilmesi icindir. (guvenlik)
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        return redirect('index')
    return render(request, 'accounts/signup.html', {'form': form})
