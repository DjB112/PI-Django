from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime, date
from portal.forms import ConsultaForm

    # Supongamos que tenemos una lista de diccionarios con registros y fechas:
registros = [
        {"codigo": 11, "url_icono": "portal/img/icon_11.png", "usuario": "Roberto Noooni", "nombre": "Nombre Proyecto 1", "detalle": "asdasdad asdasdasd asdadsa", "fecha": date(2023, 9, 23)},
        {"codigo": 12, "url_icono": "portal/img/icon_12.png", "usuario": "Carlos Yutooni", "nombre": "Nombre Proyecto 2", "detalle": "asdasdad asdasdasd asdadsa", "fecha": date(2023, 9, 21)},
        {"codigo": 13, "url_icono": "portal/img/icon_13.png", "usuario": "Juano PPooni", "nombre": "Nombre Proyecto 3", "detalle": "asdasdad asdasdasd asdadsa", "fecha": date(2023, 9, 11)},
        {"codigo": 14, "url_icono": "portal/img/icon_14.png", "usuario": "Pablo Frffooni", "nombre": "Nombre Proyecto 4", "detalle": "asdasdad asdasdasd asdadsa", "fecha": date(2023, 9, 21)},
        {"codigo": 15, "url_icono": "portal/img/icon_15.png", "usuario": "Daniel ZZooni", "nombre": "Nombre Proyecto 5", "detalle": "asdasdad asdasdasd asdadsa", "fecha": date(2023, 9, 22)},
        {"codigo": 16, "url_icono": "portal/img/icon_16.png", "usuario": "Miguel Lleoni", "nombre": "Nombre Proyecto 6", "detalle": "asdasdad asdasdasd asdadsa", "fecha": date(2023, 9, 19)},
        {"codigo": 17, "url_icono": "portal/img/icon_17.png", "usuario": "Miguuuuuel Lleoni", "nombre": "Nombre Proyecto 6", "detalle": "asdasdad asdasdasd asdadsa", "fecha": date(2023, 9, 23)},
    ]
   
# Define una función para calcular la diferencia entre la fecha actual y la fecha de cada registro
def diferencia_fecha(registro):
    # Obtén la fecha actual
    fecha_actual = date.today()
    return abs(registro["fecha"] - fecha_actual)

def indice(request):
    global registros
    # Ordena los registros por proximidad a la fecha actual
    registros_ordenados = sorted(registros, key=diferencia_fecha)
    # Selecciona los primeros 4 registros
    registros_seleccionados = registros_ordenados[:4]
    
    respuesta = render(request,"portal/index.html",{"novedades": registros_seleccionados})
    return respuesta

def proyecto(request, nro_proyecto):
    respuesta = render(request,"portal/proyecto.html",{"codigo": nro_proyecto})
    return respuesta

def busqueda(request):
    respuesta = render(request,"portal/busqueda.html")
    return respuesta

def nosotros(request):
    formulario_consultas = None
    respuesta=None

    if request.method =='GET':  # Aca es cuando carga por primera ves la pagina
        formulario_consultas= ConsultaForm()
        respuesta="no"
    elif request.method == 'POST':  # Aca hago todo lo que impacta en el sistema (envio de email, guardar datos, etc)
        formulario_consultas = ConsultaForm(request.POST)
        if formulario_consultas.is_valid():
            messages.success(request,"Hemos recibido tu consulta. Gracias")
            respuesta="si"
            
            send_mail(
                "Subject here",
                "Here is the message.",
                "from@example.com",
                ["david.j.bustamante@gmail.com"],
                fail_silently=False,
            )
             
        else:
            # se dispara un mensaje general en el campo messages al no cumplir is_valid()
            messages.error(request,"Por favor revisa los errores en el Formulario")
            respuesta="no"
                    
    else:
        return HttpResponseBadRequest("Error de datos enviados, realizar la Consulta nuevamente. Gracias")
    
    contexto={
        'ahora': datetime.now,
        'formulario': formulario_consultas,
        'respuesta' : respuesta
    }
    
    return render(request,"portal/nosotros.html",{"contexto": contexto})

def colaboracion(request):
    respuesta = render(request,"portal/colaboracion.html")
    return respuesta

def administracion(request):
    respuesta = render(request,"portal/administracion.html")
    return respuesta

def busqueda(request):
    respuesta = render(request,"portal/busqueda.html")
    return respuesta

def registrar(request):
    respuesta = render(request,"portal/registrar.html")
    return respuesta

def sesion(request):
    respuesta = render(request,"portal/sesion.html")
    return respuesta