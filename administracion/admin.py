from django.contrib import admin
from administracion.models import Novedades ,Personas,CategoriaProyectos,CategoriaColaboraciones,Proyecto,Colaboracion,Comentarios,Participaciones
# Register your models here.

admin.site.register(Personas),
admin.site.register(CategoriaProyectos),
admin.site.register(CategoriaColaboraciones),
admin.site.register(Proyecto),
admin.site.register(Colaboracion),
admin.site.register(Comentarios),
admin.site.register(Participaciones),
admin.site.register(Novedades),

@admin.action(description="Colocar Inactivos")
def ColocarInactivos(self, request, queryset):
    for proyecto in queryset:
        proyecto.SetInactivos()

@admin.action(description="Colocar Activos")        
def ColocarActivos(self, request, queryset):
    for proyecto in queryset:
        proyecto.SetActivos()

class ParticipacionesInline(admin.TabularInline):
    model = Participaciones
    
class ColaboracionAdmin(admin.ModelAdmin):
    inlines = [ParticipacionesInline,]

class ComentariosInline(admin.TabularInline):
    model = Comentarios

class ProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'personas', 'categoria', 'estado', 'fecha_creacion',)
    search_fields = ('nombre',)
    actions =[ColocarInactivos,ColocarActivos]
    inlines = [ComentariosInline,]
    
class PersonaAdmin(admin.ModelAdmin):
    list_display = ('nombre','apellido','dni','email',)
    search_fields = ('nombre', 'dni',)
    
class NovedadAdmin(admin.ModelAdmin):
    list_display = ('fecha','titulo','estado',)
    search_fields = ('titulo',)
    ordering = ('fecha',)
    actions =[ColocarInactivos,ColocarActivos]

class CategoriaProyectoAdmin(admin.ModelAdmin):
    list_display = ('nombre','estado',)
    search_fields = ('nombre',)
    actions =[ColocarInactivos,ColocarActivos]
    
class CategoriaColaboracionAdmin(admin.ModelAdmin):
    list_display = ('nombre','estado',)
    search_fields = ('nombre',)
    actions =[ColocarInactivos,ColocarActivos]     

class WebAdminSite(admin.AdminSite):
    site_header="Administracion de Cartera de Proyectos"
    site_title ="Administrador Web"
    index_title="Admin Web"
    empty_value_display = "No hay datos para visualizar"

#registro de modelos en admin personalizado
sitio_admin = WebAdminSite(name="WebAdmin")
sitio_admin.register(CategoriaProyectos, CategoriaProyectoAdmin)
sitio_admin.register(CategoriaColaboraciones, CategoriaColaboracionAdmin)
sitio_admin.register(Proyecto, ProyectoAdmin)
sitio_admin.register(Novedades, NovedadAdmin)
sitio_admin.register(Personas, PersonaAdmin)
sitio_admin.register(Colaboracion, ColaboracionAdmin)