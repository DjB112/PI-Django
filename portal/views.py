from django.shortcuts import render, HttpResponse

def indice(request):
    respuesta = HttpResponse("Pagina de Inicio")
    return respuesta
