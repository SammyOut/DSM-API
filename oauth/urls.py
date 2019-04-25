from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('login/', views.signin, name='login'),

    path('app/', views.AppListView.as_view(), name='app_list'),
    path('app/create/', views.AppCreateView.as_view(), name='app_create'),

    path('app/manage/', views.AppManageListView.as_view(), name='app_manage_list'),
    path('app/<int:app_id>', views.AppView.as_view()),

    path('service/', views.ServiceListView.as_view(), name='service_list'),

    path('oauth/login/', views.oauth_signin, name='oauth_login_view'),
    path('oauth/token/', views.generate_token, name='oauth_get_access_token'),
    path('oauth/refresh/', views.refresh_access_token, name='oauth_refresh_access_token'),

    path('info/user/', views.get_user_info, name='get_user_info'),
]
