from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),

    path('service/', views.ServiceListView.as_view(), name='service_list'),

    path('oauth/login/', views.oauth_login, name='oauth_login'),
    path('oauth/token/', views.generate_token, name='oauth_get_access_token'),
    path('oauth/refresh/', views.refresh_access_token, name='oauth_refresh_access_token'),

    path('info/user/', views.get_user_info, name='get_user_info'),
]
