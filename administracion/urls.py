from django.urls import path
from . import views as administracion_views

urlpatterns = [
    path('registrar/',administracion_views.registrar,name="registrar"),
    path('sesion/', administracion_views.sesion, name="sesion"),    
    path('',administracion_views.administracion, name="administracion"),
    path('busqueda/', administracion_views.busqueda,name="busqueda"),
    path('colaboracion/', administracion_views.colaboracion,name="colaboracion"),
    
    path('persona/',administracion_views.persona.as_view(),name="persona"),
    # path('persona/alta',administracion_views.persona_alta, name="persona_alta"),
    # path('persona/modificacion/<int:pk>',administracion_views.personas_modificacion, name="persona_modificacion"),
    # path('persona/baja/<int:pk>', administracion_views.persona_baja, name='persona_baja'),
    
]