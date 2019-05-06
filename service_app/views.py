from django.views.generic import ListView

from . import models


class ServiceListView(ListView):
    model = models.ServiceModel

    template_name = 'service/service_list.html'
    context_object_name = 'service_list'

    def get_queryset(self):
        queryset = models.ServiceModel.objects.all()
        return [queryset[a:a+3] for a in range(0, len(queryset), 3)]
