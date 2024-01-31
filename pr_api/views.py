from django.shortcuts import render
from rest_framework import viewsets, permissions
from pr_api import serializers
from administracion.models import Novedades

class NovedadesViewSet(viewsets.ModelViewSet):
    queryset= Novedades.objects.all()
    serializer_class=serializers.NovedadesSerializers
    permission_classes=[permissions.IsAuthenticated]


# Create your views here.
