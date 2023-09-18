
from django.urls import path
from . import views as portal_views

urlpatterns = [
    path('',portal_views.indice,name="indice"),
    path('cursos/<int:porte>', portal_views.cursos,name="cursos"),
]