from datetime import datetime
from json import loads
from uuid import uuid4

from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
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
        form = forms.LoginForm()

    return render(request, 'login.html', {'form': form})


def oauth_signin(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        client_id = request.POST.get('client_id')
        redirect_url = request.POST.get('redirect_url')
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
    else:
        # return render(request, 'oauth_login.html', {'form': form})
        pass


def generate_token(request):
    if request.method == 'POST':
        json_data = loads(request.body)

        token = models.TokenModel.objects.get(
            token=json_data['code'],
            app__client_id=json_data['client_id'],
            app__secret_key=json_data['secret_key'],
        )
        if token is None:
            return HttpResponse(status=204)

        access_token = f'a_{token.app.id}_{uuid4()}'
        expire_timestamp = int(datetime.now().timestamp()) + 600
        models.AccessTokenModel(
            access_token=access_token,
            app=token.app,
            student=token.student,
            expire_timestamp=expire_timestamp
        ).save()

        refresh_token = f'r_{token.app.id}_{uuid4()}'
        models.RefreshTokenModel(
            refresh_token=refresh_token,
            app=token.app,
            student=token.student,
        ).save()

        return JsonResponse({
            "access_token": access_token,
            "expire_timestamp": expire_timestamp,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        })
    else:
        return HttpResponse(status=405)


def refresh_access_token(request):
    if request.method == 'POST':
        json_data = loads(request.body)
        refresh_token = models.RefreshTokenModel.objects.get(
            app__client_id=json_data['client_id'],
            app__secret_key=json_data['secret_key'],
            refresh_token=json_data['refresh_token']
        )
        if refresh_token is None:
            return HttpResponse(status=204)

        access_token = f'a_{token.app.id}_{uuid4()}'
        expire_timestamp = int(datetime.now().timestamp()) + 600
        models.AccessTokenModel(
            access_token=access_token,
            app=refresh_token.app,
            student=refresh_token.student,
            expire_timestamp=expire_timestamp
        ).save()
        return JsonResponse({
            "access_token": access_token,
            "expire_timestamp": expire_timestamp,
            "token_type": "bearer",
        })
    else:
        return HttpResponse(status=405)


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
