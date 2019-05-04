from django.urls import path

from . import views

app_name = 'app'
urlpatterns = [
    path('', views.AppListView.as_view(), name='app_list'),
    path('create/', views.AppCreateView.as_view(), name='app_create'),
    path('manage/', views.AppManageListView.as_view(), name='app_manage_list'),
    path('manage/<int:app_id>/', views.AppManageView.as_view(), name='app_manage'),
    path('manage/<int:app_id>/delete/', views.AppDeleteView.as_view(), name='app_delete'),
    path('manage/<int:app_id>/refresh/', views.refresh_app_token, name='refresh_app_token'),
]
