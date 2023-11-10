from django.contrib import admin
from administracion.models import Personas,CategoriaProyectos,CategoriaColaboraciones,Proyecto,Colaboracion,Comentarios,Participaciones
# Register your models here.

admin.site.register(Personas),
admin.site.register(CategoriaProyectos),
admin.site.register(CategoriaColaboraciones),
admin.site.register(Proyecto),
admin.site.register(Colaboracion),
admin.site.register(Comentarios),
admin.site.register(Participaciones),

