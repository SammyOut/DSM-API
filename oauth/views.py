from datetime import datetime
from json import loads
from uuid import uuid4

from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.decorators.csrf import csrf_exempt

from const import *
from . import forms
from . import models
import exception


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
            user = auth.get_user_model().objects.create_user(**form.cleaned_data)
            auth.login(request, user)
            return redirect('main')
    else:
        form = forms.SignupForm()
    return render(request, 'signup.html', {FORM: form})


def login(request: HttpRequest):
    if request.method == POST:
        form = forms.LoginForm(request.POST)
        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('main')
    else:
        form = forms.LoginForm()
    return render(request, 'signup.html', {FORM: form})


def logout(request: HttpRequest):
    auth.logout(request)
    return redirect('main')


@csrf_exempt
def oauth_login(request: HttpRequest):
    if request.method == POST:
        client_id = request.POST.get(CLIENT_ID)
        redirect_url = request.POST.get(REDIRECT_URL)
        app = models.AppModel.objects.get(client_id=client_id)
        if app is None:
            return HttpResponse(status=404)

        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        user = auth.authenticate(username=username, password=password)
        if user is None:
            return HttpResponseRedirect(reverse('oauth_login'))

        token = f'{app.name}_{uuid4().hex}'
        models.TokenModel(
            token=token,
            student=user,
            app=app,
        ).save()
        return HttpResponseRedirect(f'{redirect_url}?code={token}')
    else:
        return render(request, 'oauth_login.html')


@csrf_exempt
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


@csrf_exempt
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

        access_token = f'a_{refresh_token.app.id}_{uuid4()}'
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


@csrf_exempt
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
    form_class = forms.AppCreateForm

    template_name = 'app_create.html'

    def form_valid(self, form):
        app = form.save(commit=False)
        app.owner = self.request.user
        app.save()

        return HttpResponseRedirect('/')

    def get_success_url(self):
        return reverse('app_manage_list')


class AppManageListView(LoginRequiredMixin, ListView):
    model = models.AppModel
    template_name = 'app_manage_list.html'
    context_object_name = 'app_list'

    def get_queryset(self):
        queryset = models.AppModel.objects.filter(owner=self.request.user)
        return [queryset[a:a+3] for a in range(0, len(queryset), 3)]


class AppManageView(LoginRequiredMixin, UpdateView):
    model = models.AppModel
    template_name = 'app_manage.html'
    context_object_name = 'app'

    fields = ('name', 'description', 'app_url',)
    pk_url_kwarg = 'app_id'

    def get_success_url(self):
        return reverse('app_manage_list')

    def dispatch(self, request, *args, **kwargs):
        app = self.get_object()
        if app.owner != self.request.user:
            raise exception.ForbiddenException()
        return super(AppManageView, self).dispatch(request, *args, **kwargs)


class AppDeleteView(LoginRequiredMixin, DeleteView):
    model = models.AppModel

    pk_url_kwarg = 'app_id'

    def get_success_url(self):
        return reverse('app_manage_list')

    def dispatch(self, request, *args, **kwargs):
        app = self.get_object()
        if app.owner != self.request.user:
            raise exception.ForbiddenException()
        return super(AppDeleteView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


def refresh_app_token(request: HttpRequest, app_id: int):
    app = models.AppModel.objects.get(id=app_id)

    if app.owner != request.user:
        raise exception.ForbiddenException()

    app.client_id = uuid4().hex
    app.secret_key = uuid4().hex
    app.save()

    return HttpResponseRedirect(reverse('app_manage_list'))


class ServiceListView(ListView):
    model = models.ServiceModel

    template_name = 'service_list.html'
    context_object_name = 'service_list'

    def get_queryset(self):
        queryset = models.ServiceModel.objects.all()
        return [queryset[a:a+3] for a in range(0, len(queryset), 3)]
