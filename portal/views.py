from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime, date
from portal.forms import ConsultaForm
from administracion.models import Novedades, Proyecto, Colaboracion
   
# Define una función para calcular la diferencia entre la fecha actual y la fecha de cada registro
def diferencia_fecha(registro):
    # Obtén la fecha actual
    fecha_actual = date.today()
    return abs(registro["fecha"] - fecha_actual)

def indice(request):
    # Selecciona los primeros 4 registros
    if (Proyecto.activos.cantidad()>4):
        proyectos_nuevos = Proyecto.activos.all()[:4]
    else:
        proyectos_nuevos = Proyecto.activos.all()
        
    reg_nov = Novedades.novedades.all()
    
    reg_col = Colaboracion.ultimacolaboracion.all().order_by('-id_colaboracion')[0]
    # nombre_col = reg_col.nombre
    
    respuesta = render(request,"portal/index.html",{"proyectos_nuevos": proyectos_nuevos,"ultima_colaboracion": reg_col,"object_list":reg_nov})
    return respuesta

def proyecto(request, nro_proyecto):
    
    respuesta = render(request,"portal/proyecto.html",{"codigo": nro_proyecto})
    return respuesta

def colaboracion(request):
        
    respuesta = render(request,"portal/colaboracion.html")
    return respuesta

def ultimacolaboracion(request,nro_colaboracion):
        
    respuesta = render(request,"portal/ultimacolaboracion.html", {"codigo": nro_colaboracion})
    return respuesta

def busqueda(request):
    respuesta = render(request,"portal/busqueda.html")
    return respuesta

def nosotros(request):
    formulario_consultas = None
    respuesta=None
    sector= ('Seleccionar','Administracion','Colaboracion','Proyectos')
    
    if request.method =='GET':  # Aca es cuando carga por primera ves la pagina
        formulario_consultas= ConsultaForm()
        respuesta="no"
    elif request.method == 'POST':  # Aca hago todo lo que impacta en el sistema (envio de email, guardar datos, etc)
        formulario_consultas = ConsultaForm(request.POST)
        if formulario_consultas.is_valid():

            mensaje = f"""De : {formulario_consultas.cleaned_data['nombre']}, {formulario_consultas.cleaned_data['apellido']} <{formulario_consultas.cleaned_data['email']}>\n 
                        Edad: {formulario_consultas.cleaned_data['edad']}\n
                        Departamento: {sector[int(formulario_consultas.cleaned_data['departamento'])]}\n 
                        Consulta: {formulario_consultas.cleaned_data['consulta']}\n
                        Suscripción: {formulario_consultas.cleaned_data['suscripcion']}\n
                        Declaración: {formulario_consultas.cleaned_data['declaracion']}\n"""
            mensaje_html = f"""
                <p>De: {formulario_consultas.cleaned_data['nombre']}, {formulario_consultas.cleaned_data['apellido']} <a href="mailto:{formulario_consultas.cleaned_data['email']}">{formulario_consultas.cleaned_data['email']}</a></p>
                <p>Edad:  {formulario_consultas.cleaned_data['edad']}</p>
                <p>Departamento:  {sector[int(formulario_consultas.cleaned_data['departamento'])]}</p>
                <p>Consulta:  {formulario_consultas.cleaned_data['consulta']}</p>
                <p>Suscripción:  {formulario_consultas.cleaned_data['suscripcion']}</p>
                <p>Declaración: {formulario_consultas.cleaned_data['declaracion']}</p>"""
            
            asunto = "CONSULTA DESDE LA PAGINA - " + sector[int(formulario_consultas.cleaned_data['departamento'])]
                
            send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [settings.RECIPIENT_ADDRESS], fail_silently=False, html_message=mensaje_html)
            
            messages.success(request,"Hemos recibido tu consulta. Gracias")
            respuesta="si"          
             
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
