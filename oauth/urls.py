from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('app/', views.AppListView.as_view()),
    path('app/<int:app_id>', views.AppView.as_view()),
    path('oauth/login/', views.oauth_signin, name='oauth_login_view'),
    path('oauth/token/', views.generate_token, name='oauth_get_access_token'),
    path('oauth/refresh/', views.refresh_access_token, name='oauth_refresh_access_token'),
    path('info/user/', views.get_user_info, name='get_user_info'),
]
