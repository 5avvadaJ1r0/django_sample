from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'auth'

urlpatterns = [
    path('', views.TopView.as_view(), name='top'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]