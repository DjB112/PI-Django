from django.shortcuts import render, HttpResponse
from datetime import datetime 

def indice(request):
    respuesta = render(request,"portal/index.html",{"ahora": datetime.now()})
    return respuesta

def cursos(request, porte):
    respuesta = HttpResponse(f"Todos los cursos {porte}")
    return respuesta
