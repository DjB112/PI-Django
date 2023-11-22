
from django.urls import path, include
from . import views as portal_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',portal_views.indice,name="indice"),
    path('nosotros/',portal_views.nosotros,name="nosotros"),
    path('proyecto/<int:nro_proyecto>',portal_views.proyecto,name="proyecto"),   
    path('colaboracion/', portal_views.colaboracion,name="colaboracion"),
    path('ultimacolaboracion/<int:nro_colaboracion>', portal_views.ultimacolaboracion,name="ultimacolaboracion"),
    path('novedad/<int:nro_novedad>', portal_views.novedad,name="novedad"),
    # path('cuentas/login/',portal_views.proyecto_login, name="proyecto_login"),
    # path('cuentas/logout/',portal_views.ProyectoLogoutView.as_view(),name="proyecto_logout"),
    # path('cuentas/logout/',auth_views.LogoutView.as_view(template_name="indice"),name="proyecto_logout"),
    path('cuentas/registrar/',portal_views.registrarse,name="registrar"),
    # path('accounts/password_change/', auth_views.PasswordChangeView.as_view(success_url="/"), name='password_change'),
    path('accounts/', include('django.contrib.auth.urls')),
]