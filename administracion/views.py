from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime, date
from administracion.forms import PersonasForm
from administracion.models import Personas, Colaboracion, Comentarios, Cuerpo, Proyecto

def registrar(request):

    if request.method=='GET':
        formulario_consultas = PersonasForm()
    elif request.method=='POST':
        formulario_consultas = PersonasForm(request.POST)
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
    respuesta = render(request,"administracion/admin.html")
    return respuesta

def colaboracion(request):
    respuesta = render(request,"administracion/colaboracion.html")
    return respuesta

def busqueda(request):
    respuesta = render(request,"administracion/busqueda.html")
    return respuesta