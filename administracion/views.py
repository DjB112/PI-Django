from typing import Any
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from datetime import datetime, date
from django.urls import reverse_lazy
from administracion.forms import NovedadesForm, PersonasForm, ComentariosForm, CategoriaFormProyectos,CategoriaFormColaboraciones, ProyectosForm, ColaboracionForm
from administracion.models import Participaciones, Novedades, Personas, Colaboracion, Comentarios, Proyecto, CategoriaProyectos,CategoriaColaboraciones
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url="proyecto_loguin")
def administracion(request):
    variable = 'Contenido de la Pagina de Inicio desde Variable del view'
    respuesta = render(request,"administracion/index.html", {'variable': variable})
    return respuesta

def busqueda(request):
    respuesta = render(request,"administracion/busqueda.html")
    return respuesta

def registrarperfil(request):
    nno = request.user.id
    kio = request.user.username
    existe_perfil = Personas.objects.filter(user_id=nno).exists()
    
    if existe_perfil :      
        # Se requiere mostrar y editar el existente
        cont=Personas.objects.get(user_id=nno)
        if (request.method == 'POST'):
            formulario = PersonasForm(request.POST, request.FILES, instance=cont)
            if formulario.is_valid():                
                formulario.save()
                messages.success(request, 'Se ha editado el curso correctamente')
                # return redirect('miperfil_index')
        else:
            formulario = PersonasForm(instance=cont)
    else:
        # Se requiere crear un perfil de cero
        if (request.method == 'POST'):
            formulario = PersonasForm(request.POST, request.FILES)
            if formulario.is_valid():               
                nombre = formulario.cleaned_data.get('nombre')
                apellido =formulario.cleaned_data.get('apellido')
                fnac = formulario.cleaned_data.get('fnac')
                dni = formulario.cleaned_data.get('dni')
                email = formulario.cleaned_data.get('email')
                estado = formulario.cleaned_data.get('estado')
                foto_perfil = formulario.cleaned_data.get('foto_perfil')
                
                miperfil = Personas(user_id= nno, nombre=nombre, apellido=apellido, fnac=fnac, dni=dni, email=email, estado=estado, foto_perfil=foto_perfil)
                miperfil.save()
                messages.success(request, 'Se ha creado el perfil correctamente')
                # return redirect('miperfil_index')
        else:
            formulario = PersonasForm()
            
                      
    return render(request, 'administracion/miperfil/alta_modificacion.html', {'form': formulario})



class NovedadListView(ListView):
    model = Novedades
    template_name = 'administracion/novedades/index.html'
    context_object_name ="categoria_list"
    queryset = Novedades.objects.all()
    ordering = ['fecha']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Novedades"
        context['url_alta'] = reverse_lazy('novedad_nueva')
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if 'titulo' in request.GET:
            self.queryset = self.queryset.filter(titulo__contains=request.GET['titulo'])
        return super().get(request, *args, **kwargs)

class NovedadCreateView(CreateView):
    model = Novedades
    form_class = NovedadesForm
    template_name = 'administracion/novedades/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('novedad_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Novedad"
        return context

class NovedadUpdateView(UpdateView):
    model = Novedades
    form_class = NovedadesForm
    template_name = 'administracion/novedades/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('novedad_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Novedad"
        return context

class NovedadDeleteView(DeleteView):
    model = Novedades
    template_name = 'administracion/novedades/baja.html'
    success_url = reverse_lazy('novedad_index')

class CategoriasproyectoListView(ListView):
    model = CategoriaProyectos
    template_name = 'administracion/categorias/categoria_list.html'
    context_object_name="categoria_list"
    queryset = CategoriaProyectos.objects.all()
    ordering = ['nombre']
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Categoria de Proyectos"
        context['url_alta'] = reverse_lazy('categoriasproyecto_nuevo')
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if 'nombre' in request.GET:
            self.queryset = self.queryset.filter(nombre__contains=request.GET['nombre'])
        return super().get(request, *args, **kwargs)

class CategoriasproyectoCreateView(CreateView):
    model = CategoriaProyectos
    form_class = CategoriaFormProyectos
    template_name = 'administracion/categorias/nuevo.html'
    context_object_name="categoria_list"
    success_url = reverse_lazy('categoriasproyecto_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Categoria de Proyectos"
        return context

class CategoriasproyectoUpdateView(UpdateView):
    model = CategoriaProyectos
    form_class = CategoriaFormProyectos
    template_name = 'administracion/categorias/nuevo.html'
    context_object_name="categoria_list"
    success_url = reverse_lazy('categoriasproyecto_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Categoria de Proyectos"
        return context

class CategoriasproyectoDeleteView(DeleteView):
    model = CategoriaProyectos
    template_name = 'administracion/categorias/eliminar.html'
    success_url = reverse_lazy('categoriasproyecto_index')

class CategoriascolaboracionListView(ListView):
    model = CategoriaColaboraciones
    template_name = 'administracion/categorias/categoria_list.html'
    context_object_name="categoria_list"
    queryset = CategoriaColaboraciones.objects.all()
    ordering = ['nombre']
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Categoria de Colaboracion"
        context['url_alta'] = reverse_lazy('categoriascolaboracion_nuevo')
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if 'nombre' in request.GET:
            self.queryset = self.queryset.filter(nombre__contains=request.GET['nombre'])
        return super().get(request, *args, **kwargs)
    
class CategoriascolaboracionCreateView(CreateView):
    model = CategoriaColaboraciones
    form_class = CategoriaFormColaboraciones
    template_name = 'administracion/categorias/nuevo.html'
    context_object_name="categoria_list"
    success_url = reverse_lazy('categoriascolaboracion_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Categoria de Colaboracion"
        context['url_atras'] = reverse_lazy('categoriascolaboracion_index')
        return context

class CategoriascolaboracionUpdateView(UpdateView):
    model = CategoriaColaboraciones
    form_class = CategoriaFormColaboraciones
    template_name = 'administracion/categorias/nuevo.html'
    context_object_name="categoria_list"
    success_url = reverse_lazy('categoriascolaboracion_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Categoria de Colaboracion"
        context['url_atras'] = reverse_lazy('categoriascolaboracion_index')
        return context

class CategoriascolaboracionDeleteView(DeleteView):
    model = CategoriaColaboraciones
    template_name = 'administracion/categorias/eliminar.html'
    success_url = reverse_lazy('categoriascolaboracion_index')

class PersonaListView(ListView):
    model = Personas
    template_name = 'administracion/abm/index.html'
    context_object_name="object_list"
    queryset = Personas.objects.all()
    ordering = ['nombre']
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Personas"
        context['url_alta'] = reverse_lazy('persona_alta')
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if 'nombre' in request.GET:
            self.queryset = self.queryset.filter(nombre__contains=request.GET['nombre'])
        return super().get(request, *args, **kwargs)

class PersonaCreateView(CreateView):
    model = Personas
    form_class = PersonasForm
    template_name = 'administracion/abm/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('persona_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Persona"
        return context

class PersonaUpdateView(UpdateView):
    model = Personas
    form_class = PersonasForm
    template_name = 'administracion/abm/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('persona_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Persona"
        return context

class PersonaDeleteView(DeleteView):
    model = Personas
    template_name = 'administracion/abm/baja.html'
    success_url = reverse_lazy('persona_index')

class ProyectoListView(ListView):
    model = Proyecto
    template_name = 'administracion/proyectos/index.html'
    context_object_name ="object_list"
    queryset = Proyecto.objects.all()
    ordering = ['nombre']
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Proyectos"
        context['url_alta'] = reverse_lazy('proyecto_alta')
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if 'nombre' in request.GET:
            self.queryset = self.queryset.filter(nombre__contains=request.GET['nombre'])
        return super().get(request, *args, **kwargs)

class ProyectoCreateView(CreateView):
    model = Proyecto
    form_class = ProyectosForm
    template_name = 'administracion/proyectos/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('proyectos_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nuevo Proyecto"
        return context
    
class ProyectoUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectosForm
    template_name = 'administracion/proyectos/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('proyectos_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Proyecto"
        return context
    
class ProyectoDeleteView(DeleteView):
    model = Proyecto
    template_name = 'administracion/proyectos/baja.html'
    success_url = reverse_lazy('proyectos_index')
    
class ColaboracionListView(ListView):
    model = Colaboracion
    template_name = 'administracion/colaboraciones/index.html'
    context_object_name ="object_list"
    queryset = Colaboracion.objects.all()
    ordering = ['nombre']
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Colaboraciones"
        context['url_alta'] = reverse_lazy('colaboracion_alta')
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if 'nombre' in request.GET:
            self.queryset = self.queryset.filter(nombre__contains=request.GET['nombre'])
        return super().get(request, *args, **kwargs)

class ColaboracionCreateView(CreateView):
    model = Colaboracion
    form_class = ColaboracionForm
    template_name = 'administracion/colaboraciones/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('colaboraciones_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Colaboración"
        return context
    
class ColaboracionUpdateView(UpdateView):
    model = Colaboracion
    form_class = ColaboracionForm
    template_name = 'administracion/colaboraciones/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('colaboraciones_index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Colaboracion"
        return context
    
class ColaboracionDeleteView(DeleteView):
    model = Colaboracion
    template_name = 'administracion/colaboraciones/baja.html'
    success_url = reverse_lazy('colaboraciones_index')
    
class ComentarioProyectoListView(ListView):
    model = Comentarios
    template_name = 'administracion/comentarios/comentarios.html'
    context_object_name ="object_list"
    queryset=Comentarios.objects.filter(tipo = 'PRO')
    ordering = ['fecha_creacion']
    
    def get_queryset(self):
      return super(ComentarioProyectoListView,self).get_queryset().filter(nro_proyecto=self.kwargs.get("pk"))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombreproyecto'] = 'Comentarios del Proyecto: ' + Proyecto.objects.get(id_proyecto=self.kwargs.get("pk")).nombre
        context['ident'] = self.kwargs.get("pk")
        context['titulo'] = "Comentarios"
        return context

class ComentarioProyectoUpdateView(UpdateView):
    model = Comentarios
    form_class = ComentariosForm
    template_name = 'administracion/comentarios/alta_modificacion.html'
    context_object_name="object_list"
    
    def get_success_url(self, **kwargs):   
            return reverse_lazy('comentarios_proyecto', kwargs={'pk': self.object.nro_proyecto_id}) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Comentario"
        return context

    
class ComentarioProyectoDeleteView(DeleteView):
    model = Comentarios
    template_name = 'administracion/comentarios/comentarios_baja.html'

    def get_success_url(self, **kwargs):   
            return reverse_lazy('comentarios_proyecto', kwargs={'pk': self.object.nro_proyecto_id})    

class MisProyectosListView(ListView):
    model = Proyecto
    template_name = 'administracion/misproyectos/index.html'
    context_object_name ="object_list"
    # idpersona = Personas.objects.filter()
    
    def get_queryset(self):
        # fuy = Personas.objects.get(user=self.request.user).id_personas
        try:
            fuy = Personas.objects.get(user=self.request.user).id_personas    
            val = Proyecto.objects.filter(personas_id= fuy)
        except Personas.DoesNotExist:
            val = None
        return val 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            fuy = Personas.objects.get(user=self.request.user).id_personas    
            val = Proyecto.objects.filter(personas_id= fuy)
            context['titulo'] = "Mis Proyectos"
            context['url_alta'] = reverse_lazy('misproyectos_alta')
        except Personas.DoesNotExist:
            context['titulo'] = "Mis Proyectos: Debe Primero Cargar su Perfil"
            # context['url_alta'] = reverse_lazy('misproyectos_alta')      
        return context

class MisProyectosCreateView(CreateView):
    model = Proyecto
    form_class = ProyectosForm
    template_name = 'administracion/misproyectos/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('misproyectos_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nuevo Proyecto"
        
        try:
            personas = Personas.objects.get(user=self.request.user).id_personas
        except Personas.DoesNotExist:
            context= None
            
        return context

class MisProyectosUpdateView(UpdateView):
    model = Proyecto
    form_class = ProyectosForm
    template_name = 'administracion/misproyectos/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('misproyectos_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Proyecto"
        
        try:
            personas = Personas.objects.get(user=self.request.user).id_personas
        except Personas.DoesNotExist:
            context= None
            
        return context

class MisProyectosDeleteView(DeleteView):
    model = Proyecto
    template_name = 'administracion/misproyectos/baja.html'
    success_url = reverse_lazy('misproyectos_index')
    
    
class MisColaboracionesListView(ListView):
    model = Colaboracion
    template_name = 'administracion/miscolaboraciones/index.html'
    context_object_name ="object_list"
    # idpersona = Personas.objects.filter()
    
    def get_queryset(self):
        # fuy = Personas.objects.get(user=self.request.user).id_personas
        try:
            fuy = Personas.objects.get(user=self.request.user).id_personas    
            ret = Participaciones.objects.get(persona_id=fuy).colaboracion_id
            val = Colaboracion.objects.filter(id_colaboracion = ret)
        except Personas.DoesNotExist:
            val = None
        except Participaciones.DoesNotExist:
            val = None
        return val 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            fuy = Personas.objects.get(user=self.request.user).id_personas    
            ret = Participaciones.objects.get(persona_id=fuy).colaboracion_id
            val = Colaboracion.objects.filter(id_colaboracion = ret)
            context['titulo'] = "Mis Colaboraciones"
            context['url_alta'] = reverse_lazy('miscolaboraciones_alta')
        except Personas.DoesNotExist:
            context['titulo'] = "Mis Colaboraciones: Debe Primero Cargar su Perfil"
            # context['url_alta'] = reverse_lazy('misproyectos_alta')
        except Participaciones.DoesNotExist:
            context['titulo'] = "Mis Colaboraciones"      
        return context

class MisColaboracionesCreateView(CreateView):
    model = Colaboracion
    form_class = ColaboracionForm
    template_name = 'administracion/miscolaboraciones/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('miscolaboraciones_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Colaboración"
        
        try:
            personas = Personas.objects.get(user=self.request.user).id_personas
        except Personas.DoesNotExist:
            context= None
            
        return context   

class MisColaboracionesUpdateView(UpdateView):
    model = Colaboracion
    form_class = ColaboracionForm
    template_name = 'administracion/miscolaboraciones/alta_modificacion.html'
    context_object_name="object_list"
    success_url = reverse_lazy('miscolaboraciones_index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Modificar Colaboración"
        
        try:
            personas = Personas.objects.get(user=self.request.user).id_personas
        except Personas.DoesNotExist:
            context= None
            
        return context

class MisColaboracionesDeleteView(DeleteView):
    model = Colaboracion
    template_name = 'administracion/miscolaboraciones/baja.html'
    success_url = reverse_lazy('miscolaboraciones_index')