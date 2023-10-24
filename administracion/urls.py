from django.urls import path
from . import views as administracion_views

urlpatterns = [
    path('registrar/',administracion_views.registrar,name="registrar"),
    path('sesion/', administracion_views.sesion, name="sesion"),    
    path('administracion/',administracion_views.administracion, name="administracion"),
    path('busqueda/', administracion_views.busqueda,name="busqueda"),
    path('colaboracion/', administracion_views.colaboracion,name="colaboracion"),
]