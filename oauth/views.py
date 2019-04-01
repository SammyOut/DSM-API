from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import redirect, render

from . import forms


def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():

            user = get_user_model().objects.createuser(**form.cleaned_data)
            login(request, user)
            # return redirect()
    else:
        form = forms.SignupForm()
    # return render()


def signin(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # return redirect()
    else:
        form = forms.LoginForm

    # return render()
