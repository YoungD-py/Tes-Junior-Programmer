"""
URL Configuration untuk app products.
Includes REST API endpoints dan web views.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Initialize router untuk REST API viewsets
router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='api-product')
router.register(r'kategoris', views.KategoriViewSet, basename='api-kategori')
router.register(r'statuses', views.StatusViewSet, basename='api-status')

# Web URLs
urlpatterns = [
    # Product Web Views (CRUD)
    path('', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # API Fetch
    path('fetch-api/', views.fetch_api_data, name='fetch_api'),
]

# Include API URLs
urlpatterns += [
    path('api/', include(router.urls)),
]
