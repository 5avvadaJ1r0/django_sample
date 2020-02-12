from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ShopListView.as_view(), name='list'),
    path('create/', views.ShopCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ShopUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', views.ShopDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.ShopViewSet.as_view({'delete': 'destroy'}), name='delete'),
    path('image/list/<int:pk>/', views.ShopImageView.as_view(), name='image_list'),
    path('image/order/<int:pk>/', views.ShopImageViewSet.as_view({'post': 'update_order'}), name='image_order'),

    path('image/thumbnail/upload/<int:pk>/', views.ShopImageViewSet.as_view({'post': 'create'}), name='image_upload'),
    path('image/thumbnail/remove/<int:pk>/', views.ShopImageViewSet.as_view({'delete': 'destroy'}), name='image_remove'),
    path('image/thumbnails/<int:pk>/', views.ShopImageViewSet.as_view({'get': 'list'}), name='image_thumbnails'),
    path('image/thumbnail/<int:pk>/', views.ShopImageViewSet.as_view({'get': 'retrieve'}), name='image_thumbnail'),
]
