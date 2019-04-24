from datetime import datetime
from json import loads
from uuid import uuid4

from django.http import HttpRequest
from django.contrib.auth import login, authenticate, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import View, ListView, CreateView

from const import *
from . import forms
from . import models


def main(request: HttpRequest):
    return render(request, 'main.html')


def signup(request: HttpRequest):
    if request.method.upper() == POST:
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data[PASSWORD] = data[PASSWORD1]
            del data[PASSWORD1]
            del data[PASSWORD2]
            user = get_user_model().objects.create_user(**form.cleaned_data)
            login(request, user)
            return redirect('main')
    else:
        form = forms.SignupForm()
    return render(request, 'signup.html', {FORM: form})


def signin(request: HttpRequest):
    if request.method == POST:
        form = forms.LoginForm(request.POST)
        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
    else:
        form = forms.LoginForm()
    return render(request, 'signup.html', {FORM: form})


def signout(request: HttpRequest):
    logout(request)
    return redirect('main')


def oauth_signin(request: HttpRequest):
    if request.method == POST:
        form = forms.LoginForm(request.POST)
        client_id = request.POST.get(CLIENT_ID)
        redirect_url = request.POST.get(REDIRECT_URL)
        app = models.AppModel.objects.get(client_id=client_id)
        if app is None:
            # redirect()
            pass

        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        user = authenticate(username=username, password=password)
        if user is None:
            # redirect()
            pass

        models.TokenModel(
            token=username + client_id,  # TODO: hash 값으로
            student=user,
            app=app,
        ).save()
        # redirect(redirect_url?code=token)
    else:
        # return render(request, 'oauth_login.html', {'form': form})
        pass


def generate_token(request: HttpRequest):
    if request.method == POST:
        json_data = loads(request.body)

        token = models.TokenModel.objects.get(
            token=json_data[CODE],
            app__client_id=json_data[CLIENT_ID],
            app__secret_key=json_data[SECRET_KEY],
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
            ACCESS_TOKEN: access_token,
            EXPIRE_TIMESTAMP: expire_timestamp,
            REFRESH_TOKEN: refresh_token,
            TOKEN_TYPE: BEARER,
        })
    else:
        return HttpResponse(status=405)


def refresh_access_token(request: HttpRequest):
    if request.method == POST:
        json_data = loads(request.body)
        refresh_token = models.RefreshTokenModel.objects.get(
            app__client_id=json_data[CLIENT_ID],
            app__secret_key=json_data[SECRET_KEY],
            refresh_token=json_data[REFRESH_TOKEN]
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
            ACCESS_TOKEN: access_token,
            EXPIRE_TIMESTAMP: expire_timestamp,
            TOKEN_TYPE: BEARER,
        })
    else:
        return HttpResponse(status=405)


def get_user_info(request: HttpRequest):
    if request.method == GET:
        access_token = request.META.get(HTTP_AUTHORIZATION).split()
        if access_token[0].lower() != BEARER:
            return HttpResponse(status=422)

        access_token = models.AccessTokenModel.objects.get(access_token=access_token[1])
        if datetime.now().timestamp() > access_token.expire_timestamp:
            access_token.delete()
            return HttpResponse(status=422)

        student = access_token.student
        return JsonResponse({
            NAME: student.name,
            NUMBER: student.number,
            UUID: student.uuid,
        })
    else:
        return HttpResponse(status=405)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AppListView(ListView):
    model = models.AppModel
    template_name = 'app_list.html'
    context_object_name = 'app_list'

    def get_queryset(self):
        queryset = models.AppModel.objects.all()
        return [queryset[a:a+3] for a in range(0, len(queryset), 3)]


class AppCreateView(LoginRequiredMixin, CreateView):
    model = models.AppModel


class AppView(LoginRequiredMixin, View):  # TODO: App View 구현
    def get(self, request: HttpRequest, app_id):
        app = models.AppModel.objects.get(id=app_id, owner=request.user)
        # return render()

    def delete(self, request: HttpRequest, app_id):
        models.AppModel.objects.get(id=app_id, owner=request.user).delete()
        # return redirect()


class ServiceListView(LoginRequiredMixin, ListView):
    model = models.ServiceModel

    template_name = 'service_list.html'
    context_object_name = 'service_list'

    def get_queryset(self):
        queryset = models.ServiceModel.objects.all()
        return [queryset[a:a+3] for a in range(0, len(queryset), 3)]
