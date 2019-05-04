from django.contrib import auth
from django.http import HttpRequest
from django.shortcuts import render, redirect

from const import *
from . import forms


def signup(request: HttpRequest):
    if request.method.upper() == POST:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data[PASSWORD] = data[PASSWORD1]
            del data[PASSWORD1]
            del data[PASSWORD2]
            user = auth.get_user_model().objects.create_user(**form.cleaned_data)
            auth.login(request, user)
            return redirect('main')
    else:
        form = forms.SignupForm()
    return render(request, 'account/signup.html', {FORM: form})


def login(request: HttpRequest):
    if request.method == POST:
        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main')
        return redirect('main')


def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('main')
