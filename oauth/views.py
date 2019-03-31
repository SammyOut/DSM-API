from django.contrib.auth import login, authenticate, get_user_model
from django.shortcuts import redirect, render

from . import forms


def signup(request):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = get_user_model().objects.createuser(**form.cleaned_data)
            login(request, user)
            # return redirect()
    else:
        form = forms.SignupForm
    # return render()