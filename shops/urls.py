from django.urls import path
from . import views
from shops.views import ShopViewSet

app_name = 'shop'

urlpatterns = [
    path('', views.ShopListView.as_view(), name='list'),
    path('create/', views.ShopCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ShopUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', views.ShopDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.ShopViewSet.as_view({'delete': 'destroy'}), name='delete'),
    path('image/<int:pk>/', views.ShopImageView.as_view(), name='image'),
]
