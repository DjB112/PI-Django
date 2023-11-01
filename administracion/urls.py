from django.urls import path
from . import views as administracion_views

urlpatterns = [
    path('registrar/',administracion_views.registrar,name="registrar"),
    path('sesion/', administracion_views.sesion, name="sesion"),    
    path('',administracion_views.administracion, name="administracion"),
    path('busqueda/', administracion_views.busqueda,name="busqueda"),
    path('colaboracion/', administracion_views.colaboracion,name="colaboracion"),
    
    path('persona/',administracion_views.PersonaListView.as_view(),name="persona_index"),
    path('persona/alta',administracion_views.PersonaCreateView.as_view(), name="persona_alta"),
    path('persona/modificacion/<int:pk>',administracion_views.PersonaUpdateView.as_view(), name="persona_modificacion"),
    path('persona/baja/<int:pk>', administracion_views.PersonaDeleteView.as_view(), name='persona_baja'),
    
]