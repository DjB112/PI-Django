
from django.urls import path
from . import views as portal_views

urlpatterns = [
    path('',portal_views.indice,name="indice"),
    path('nosotros/',portal_views.nosotros,name="nosotros"),
    path('proyecto/<int:nro_proyecto>',portal_views.proyecto,name="proyecto"),   
    path('colaboracion/', portal_views.colaboracion,name="colaboracion"),
    path('ultimacolaboracion/<int:nro_colaboracion>', portal_views.ultimacolaboracion,name="ultimacolaboracion"),
]