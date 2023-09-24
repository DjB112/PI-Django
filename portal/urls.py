
from django.urls import path
from . import views as portal_views

urlpatterns = [
    path('',portal_views.indice,name="indice"),
    path('busqueda/', portal_views.busqueda,name="busqueda"),
    path('colaboracion/', portal_views.colaboracion,name="colaboracion"),
    path('nosotros/',portal_views.nosotros,name="nosotros"),
    path('administracion/',portal_views.administracion, name="administracion"),
    path('sesion/',portal_views.sesion,name="sesion"),
    path('registrar/',portal_views.registrar,name="registrar"),
    path('proyecto/<int:nro_proyecto>',portal_views.proyecto,name="proyecto"),
]