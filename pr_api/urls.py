from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pr_api import views 

mi_router = DefaultRouter()
mi_router.register('novedades', views.NovedadesViewSet, basename='novedades')

urlpatterns = [
    path('',include(mi_router.urls)),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]