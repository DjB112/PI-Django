from typing import Any
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from datetime import datetime, date
from django.urls import reverse_lazy
from administracion.forms import PersonasForm
from administracion.models import Personas, Colaboracion, Comentarios, Cuerpo, Proyecto, Categoria

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
    variable = 'No inspirarse en este proyecto ;)'
    respuesta = render(request,"administracion/index.html", {'variable': variable})
    return respuesta

def colaboracion(request):
    respuesta = render(request,"administracion/colaboracion.html")
    return respuesta

def busqueda(request):
    respuesta = render(request,"administracion/busqueda.html")
    return respuesta

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