from django.urls import path
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='signout'),
    path('login/', views.login, name='login'),

    path('app/', views.AppListView.as_view(), name='app_list'),
    path('app/create/', views.AppCreateView.as_view(), name='app_create'),
    path('app/manage/', views.AppManageListView.as_view(), name='app_manage_list'),
    path('app/manage/<int:app_id>/', views.AppManageView.as_view(), name='app_manage'),
    path('app/manage/<int:app_id>/delete/', views.AppDeleteView.as_view(), name='app_delete'),
    path('app/manage/<int:app_id>/refresh/', views.refresh_app_token, name='refresh_app_token'),

    path('service/', views.ServiceListView.as_view(), name='service_list'),

    path('oauth/login/', views.oauth_login, name='oauth_login'),
    path('oauth/token/', views.generate_token, name='oauth_get_access_token'),
    path('oauth/refresh/', views.refresh_access_token, name='oauth_refresh_access_token'),

    path('info/user/', views.get_user_info, name='get_user_info'),
]
