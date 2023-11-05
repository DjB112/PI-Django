from typing import Any
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from datetime import datetime, date
from django.urls import reverse_lazy
from administracion.forms import PersonasForm, CategoriaFormProyectos,CategoriaFormColaboraciones, ProyectosForm, ColaboracionForm
from administracion.models import Personas, Colaboracion, Comentarios, Cuerpo, Proyecto, CategoriaProyectos,CategoriaColaboraciones

def registrar(request):

    if request.method=='GET':
        formulario_consultas = PersonasForm()
    elif request.method=='POST':
        formulario_consultas = PersonasForm(request.POST,request.FILES)
        if formulario_consultas.is_valid():
            nombre= formulario_consultas.cleaned_data['nombre']
            apellido=formulario_consultas.cleaned_data['apellido']
            fnac=formulario_consultas.cleaned_data['fnac']
            dni=formulario_consultas.cleaned_data['dni']
            email=formulario_consultas.cleaned_data['email']
            estado=formulario_consultas.cleaned_data['estado']
            foto_perfil=formulario_consultas.cleaned_data['foto_perfil']
            nueva_persona = Personas(nombre=nombre, apellido=apellido, fnac= fnac, dni=dni, email=email,estado=estado,foto_perfil=foto_perfil)
            nueva_persona.save()
            messages.success(request,"Hemos recibido su registro. Gracias")
    else:
        messages.error(request,"Por favor revisa los errores en el Formulario")
    
    respuesta = render(request,"administracion/registrar.html", {"formulario_personas": formulario_consultas})
    return respuesta

def sesion(request):
    respuesta = render(request,"administracion/sesion.html")
    return respuesta

def administracion(request):
    variable = 'Contenido de la Pagina de Inicio desde Variable del view'
    respuesta = render(request,"administracion/index.html", {'variable': variable})
    return respuesta

def colaboracion(request):
    respuesta = render(request,"administracion/colaboracion.html")
    return respuesta

def busqueda(request):
    respuesta = render(request,"administracion/busqueda.html")
    return respuesta

class CategoriasproyectoListView(ListView):
    model = CategoriaProyectos
    template_name = 'administracion/categoria_list.html'
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
    template_name = 'administracion/categoria_list.html'
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