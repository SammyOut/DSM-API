from django.urls import path
from . import views


app_name = 'oauth'
urlpatterns = [
    path('service/', views.ServiceListView.as_view(), name='service_list'),

    path('login/', views.oauth_login, name='oauth_login'),
    path('token/', views.generate_token, name='oauth_get_access_token'),
    path('refresh/', views.refresh_access_token, name='oauth_refresh_access_token'),

    path('info/user/', views.get_user_info, name='get_user_info'),
]
