from datetime import datetime
from json import loads
from uuid import uuid4

from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import auth
from django.shortcuts import render, reverse

from django.views.decorators.csrf import csrf_exempt

from app_app.models import AppModel
from const import *

from . import models


@csrf_exempt
def oauth_login(request: HttpRequest):
    if request.method == POST:
        client_id = request.POST.get(CLIENT_ID, None) or request.GET.get(CLIENT_ID, None)
        redirect_url = request.POST.get(REDIRECT_URL, None) or request.GET.get(REDIRECT_URL, None)
        app = AppModel.objects.get(client_id=client_id)
        if app is None:
            return HttpResponse(status=404)

        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        user = auth.authenticate(username=username, password=password)
        if user is None:
            return HttpResponseRedirect(reverse('oauth:oauth_login'), status=403)

        token = f'{app.name}_{uuid4().hex}'
        models.TokenModel(
            token=token,
            student=user,
            app=app,
        ).save()
        return HttpResponseRedirect(f'{redirect_url}?code={token}')
    else:
        return render(request, 'oauth/oauth_login.html')


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


