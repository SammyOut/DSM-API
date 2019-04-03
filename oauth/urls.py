from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.signin, name='login'),
    path('app/', views.AppListView),
    path('oauth/login/', views.oauth_signin, name='oauth_login_view'),
    # path('oauth/token/'),
    # path('oauth/refresh/'),
]
