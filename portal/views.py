from django.shortcuts import render, HttpResponse
from datetime import datetime 

import datetime

# Define una función para calcular la diferencia entre la fecha actual y la fecha de cada registro
def diferencia_fecha(registro):
    # Obtén la fecha actual
    fecha_actual = datetime.date.today()
    return abs(registro["fecha"] - fecha_actual)

def indice(request):
    # Supongamos que tienes una lista de diccionarios con registros y fechas:
    registros = [
        {"codigo": 11, "url_icono": "portal/img/icon_11.png", "usuario": "Roberto Noooni", "nombre": "Nombre Proyecto 1", "detalle": "asdasdad asdasdasd asdadsa", "fecha": datetime.date(2023, 9, 23)},
        {"codigo": 12, "url_icono": "portal/img/icon_12.png", "usuario": "Carlos Yutooni", "nombre": "Nombre Proyecto 2", "detalle": "asdasdad asdasdasd asdadsa", "fecha": datetime.date(2023, 9, 21)},
        {"codigo": 13, "url_icono": "portal/img/icon_13.png", "usuario": "Juano PPooni", "nombre": "Nombre Proyecto 3", "detalle": "asdasdad asdasdasd asdadsa", "fecha": datetime.date(2023, 9, 11)},
        {"codigo": 14, "url_icono": "portal/img/icon_14.png", "usuario": "Pablo Frffooni", "nombre": "Nombre Proyecto 4", "detalle": "asdasdad asdasdasd asdadsa", "fecha": datetime.date(2023, 9, 21)},
        {"codigo": 15, "url_icono": "portal/img/icon_15.png", "usuario": "Daniel ZZooni", "nombre": "Nombre Proyecto 5", "detalle": "asdasdad asdasdasd asdadsa", "fecha": datetime.date(2023, 9, 22)},
        {"codigo": 16, "url_icono": "portal/img/icon_16.png", "usuario": "Miguel Lleoni", "nombre": "Nombre Proyecto 6", "detalle": "asdasdad asdasdasd asdadsa", "fecha": datetime.date(2023, 9, 19)},
        {"codigo": 17, "url_icono": "portal/img/icon_17.png", "usuario": "Miguuuuuel Lleoni", "nombre": "Nombre Proyecto 6", "detalle": "asdasdad asdasdasd asdadsa", "fecha": datetime.date(2023, 9, 23)},
    ]
   
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
    respuesta = render(request,"portal/nosotros.html")
    return respuesta

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