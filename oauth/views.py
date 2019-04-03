from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import View, ListView, CreateView

from . import forms
from . import models


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
            login(request, user)
            # return redirect()
    else:
        form = forms.LoginForm

    return render(request, 'login.html', {'form': form})


def oauth_signin(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        client_id = request.POST.get('client_id')
        app = models.AppModel.objects.get(client_id=client_id)
        if app is None:
            # redirect()
            pass

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is None:
            # redirect()
            pass

        models.TokenModel(
            token=username+client_id,  # TODO: hash 값으로
            student=user,
            app=app,
        ).save()
        # redirect(redirect_url?code=token)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AppListView(LoginRequiredMixin, ListView):
    model = models.AppModel


class AppCreateView(LoginRequiredMixin, CreateView):
    model = models.AppModel


class AppView(LoginRequiredMixin, View):  # TODO: App View 구현
    def get(self, request):
        pass

    def delete(self, request):
        pass

    def patch(self, request):
        pass


class ServiceListView(LoginRequiredMixin, ListView):
    model = models.ServiceModel
