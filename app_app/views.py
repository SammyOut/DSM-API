from uuid import uuid4

from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from . import forms
from . import models
import exception


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AppListView(ListView):
    model = models.AppModel
    template_name = 'app/app_list.html'
    context_object_name = 'app_list'

    def get_queryset(self):
        queryset = models.AppModel.objects.all()
        return [queryset[a:a+3] for a in range(0, len(queryset), 3)]


class AppCreateView(LoginRequiredMixin, CreateView):
    model = models.AppModel
    form_class = forms.AppCreateForm

    template_name = 'app/app_create.html'

    def form_valid(self, form):
        app = form.save(commit=False)
        app.owner = self.request.user
        app.save()

        return HttpResponseRedirect('/')

    def get_success_url(self):
        return reverse('app:app_manage_list')


class AppManageListView(LoginRequiredMixin, ListView):
    model = models.AppModel
    template_name = 'app/app_manage_list.html'
    context_object_name = 'app_list'

    def get_queryset(self):
        queryset = models.AppModel.objects.filter(owner=self.request.user)
        return [queryset[a:a+3] for a in range(0, len(queryset), 3)]


class AppManageView(LoginRequiredMixin, UpdateView):
    model = models.AppModel
    template_name = 'app/app_manage.html'
    context_object_name = 'app'

    fields = ('name', 'description', 'app_url',)
    pk_url_kwarg = 'app_id'

    def get_success_url(self):
        return reverse('app:app_manage_list')

    def dispatch(self, request, *args, **kwargs):
        app = self.get_object()
        if app.owner != self.request.user:
            raise exception.ForbiddenException()
        return super(AppManageView, self).dispatch(request, *args, **kwargs)


class AppDeleteView(LoginRequiredMixin, DeleteView):
    model = models.AppModel

    pk_url_kwarg = 'app_id'

    def get_success_url(self):
        return reverse('app:app_manage_list')

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

    return HttpResponseRedirect(reverse('app:app_manage_list'))
