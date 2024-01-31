from rest_framework import serializers
from administracion.models import Novedades

class NovedadesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Novedades
        fields = [
            'id_novedad','titulo','mensaje','estado','fecha','contenido','imagen'
            ]