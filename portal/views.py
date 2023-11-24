from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from datetime import datetime, date
from portal.forms import ConsultaForm, RegistrarUsuarioForm
from administracion.models import Novedades, Proyecto, Colaboracion,Comentarios
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LogoutView
from administracion.forms import PersonasForm
from administracion.models import Personas
   
# Define una función para calcular la diferencia entre la fecha actual y la fecha de cada registro
def diferencia_fecha(registro):
    # Obtén la fecha actual
    fecha_actual = date.today()
    return abs(registro["fecha"] - fecha_actual)

def fun_banner():
    # Selecciona las ultimas 4 novedades
    if (Proyecto.activos.cantidad()>4):
        proyectos_nuevos = Proyecto.activos.all()[:4]
    elif (Proyecto.activos.cantidad()>0):
        proyectos_nuevos = Proyecto.activos.all()
    else:
        proyectos_nuevos = None
    # Verificamos que exista alguna novedad
    if (Novedades.novedades.cantidad()>0):    
        reg_nov = Novedades.novedades.all()
    else:
        reg_nov = None
    # Selecciona la colaboracion mas nueva
    if (Colaboracion.ultimacolaboracion.cantidad()>0):
        reg_col = Colaboracion.ultimacolaboracion.all().order_by('-id_colaboracion')[0]
    else:
        reg_col = None
        
    return proyectos_nuevos, reg_nov, reg_col
    
def indice(request):
    resultado = fun_banner()
    proyectos_nuevos = resultado[0]
    reg_nov = resultado[1]
    reg_col = resultado[2]
        
    respuesta = render(request,"portal/index.html",{"proyectos_nuevos": proyectos_nuevos,"ultima_colaboracion": reg_col,"object_list":reg_nov})
    return respuesta

def proyecto(request, nro_proyecto):
    pro_objeto = Proyecto.objects.filter(id_proyecto= nro_proyecto).get()
    pro_comentario = Comentarios.objects.filter(nro_proyecto = nro_proyecto, tipo="PRO", estado=True)
    try:
        respuesta = render(request,"portal/proyecto.html",{"pro_comentario": pro_comentario, "pro_objeto": pro_objeto})
    except Comentarios.DoesNotExist:
        respuesta = render(request,"portal/proyecto.html",{"pro_objeto": pro_objeto})
    return respuesta

def busqueda(request):

    pro_objeto=Proyecto.objects.filter(estado=True)
    respuesta = render(request,"portal/busqueda.html",{"pro_objeto": pro_objeto})
    return respuesta
    
def colaboracion(request):
    resultado = fun_banner()
    proyectos_nuevos = resultado[0]
    reg_nov = resultado[1]
    reg_col = resultado[2]    
    col_objeto=Colaboracion.objects.filter(estado=True)

    respuesta = render(request,"portal/colaboracion.html",{"proyectos_nuevos": proyectos_nuevos,"ultima_colaboracion": reg_col,"object_list":reg_nov, "col_objeto": col_objeto})
    return respuesta

def ultimacolaboracion(request,nro_colaboracion):
    resultado = fun_banner()
    proyectos_nuevos = resultado[0]
    reg_nov = resultado[1]
    reg_col = resultado[2]           
    
    col_objeto = Colaboracion.objects.filter(id_colaboracion= nro_colaboracion).get()
    col_comentario = Comentarios.objects.filter(nro_proyecto = nro_colaboracion, tipo="COL", estado=True)
    try:
        respuesta = render(request,"portal/ultimacolaboracion.html",{"col_comentario": col_comentario, "col_objeto": col_objeto, "proyectos_nuevos": proyectos_nuevos,"ultima_colaboracion": reg_col,"object_list":reg_nov})
    except Comentarios.DoesNotExist:
        respuesta = render(request,"portal/ultimacolaboracion.html",{"col_objeto": col_objeto, "proyectos_nuevos": proyectos_nuevos,"ultima_colaboracion": reg_col,"object_list":reg_nov})
    
    # respuesta = render(request,"portal/ultimacolaboracion.html", {"codigo": nro_colaboracion, "proyectos_nuevos": proyectos_nuevos,"ultima_colaboracion": reg_col,"object_list":reg_nov})
    return respuesta

def novedad(request,nro_novedad):
        
    respuesta = render(request,"portal/novedad.html", {"codigo": nro_novedad})
    return respuesta

def nosotros(request):
    resultado = fun_banner()
    proyectos_nuevos = resultado[0]
    reg_nov = resultado[1]
    reg_col = resultado[2]  
    
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
    
    return render(request,"portal/nosotros.html",{"contexto": contexto,"proyectos_nuevos": proyectos_nuevos,"ultima_colaboracion": reg_col,"object_list":reg_nov})

def proyecto_login(request):
    if request.method == 'POST':
        # AuthenticationForm_can_also_be_used__
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' Bienvenido/a {username} !!')
            return redirect('indice')
        else:
            messages.error(request, f'Cuenta o password incorrecto, realice el login correctamente')
    form = AuthenticationForm()
    return render(request, 'portal/login.html', {'form': form, 'title': 'Log in'})

class ProyectoLogoutView(LogoutView):
    next_page = 'indice'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, 'Se ha cerrado la session correctamente.')
        return response
    
def registrarse(request):
    if request.method == 'POST':
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # user = User.objects.get(username=user.username)
            group = Group.objects.get(name='registrados')
            user.groups.add(group)
            # username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')       
            messages.success(
                request, f'Tu cuenta fue creada con éxito! No te olvides de completar tu Perfil desde el Panel. Ya te podes loguear en el sistema.')
            return redirect('login')
    else:
        form = RegistrarUsuarioForm()
    return render(request, 'portal/registrar.html', {'form': form, 'title': 'registrese aquí'})
