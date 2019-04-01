from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import redirect, render

from . import forms


def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['password'] = data['password1']
            del data['password1']
            del data['password2']
            user = get_user_model().objects.create_user(**form.cleaned_data)
            login(request, user)
            return redirect()
    else:
        form = forms.SignupForm()
    return render(request, 'signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            print('success')
            login(request, user)
            # return redirect()
        print('failed')
    else:
        form = forms.LoginForm

    return render(request, 'login.html', {'form': form})
