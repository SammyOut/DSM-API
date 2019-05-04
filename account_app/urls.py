from django.urls import path
from . import views


app_name = 'account'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='signout'),
    path('login/', views.login, name='login'),
]
