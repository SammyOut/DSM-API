from django.urls import path
from . import views

app_name = 'service'
urlpatterns = [
    path('', views.ServiceListView.as_view(), name='service_list'),
]
