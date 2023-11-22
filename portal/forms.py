from django import forms
from django.forms import ValidationError
from administracion.forms import PersonasForm
from administracion.models import Personas
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re

# Realizo una validacion sobre los campos que solo pueden ser letras
def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre no puede contener números. %(valor)s',
                              code='Invalid',
                              params={'valor': value})

#  Realizo una validacion dobre el campo mail para que no se utilice simbolos incorrectos
def custom_validate_email(value):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, value):
        raise ValidationError('Correo electrónico inválido')

class ConsultaForm (forms.Form):
    sector= (
        ('','Seleccionar'),
        (1,'Administracion'),
        (2,'Colaboracion'),
        (3,'Proyectos')
    )
    
    nombre = forms.CharField(
        label="Nombre:",
        max_length=20, 
        required=True,
        validators=(solo_caracteres,), 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa tu nombre'})
        )
    apellido = forms.CharField(
        label="Apellido:", 
        max_length=20,
        required=True,
        validators=(solo_caracteres,),
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa tu Apellido'})
        )
    email = forms.EmailField(
        label="Email:",
        max_length=50,
        required=True,
        validators=(custom_validate_email,),
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa tu email','type':'email'})
        )
    edad = forms.IntegerField(
        label="Edad:", 
        required=True, 
        min_value=1, 
        max_value=90, 
        widget=forms.NumberInput(attrs={'class':'form-control w-25','placeholder':'Ingresa tu edad'})
        )
    departamento = forms.ChoiceField(
        label="Departamento:",
        choices= sector,
        required=True,
        widget=forms.Select(attrs={'class':'form-control','placeholder':''})
    )
    consulta = forms.CharField(
        label="Consulta:", 
        required=True,
        max_length=200, 
        widget=forms.Textarea(attrs={'rows':10, 'class':'form-control','placeholder':'Ingresa tu consulta máximo 200 caracteres.'})
        )
    suscripcion= forms.BooleanField(
        label="Deseo suscribirme a las novedades de Carpeta de Proyectos",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'value': 1})
        )     
    declaracion=forms.BooleanField(
        label="Me Declaro responsable de todo la informacion enviada",
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'value': 1})
    )
    
    # Si el mensaje tiene menos de 10 caracteres no resulta claro
    def clean_consulta(self):
        data = self.cleaned_data['consulta']
        if len(data) < 10:
            raise ValidationError(
                "Debes especificar mejor el mensaje que nos envias")
        return data
    
    #  Si la persona tiene menos de 18 años no puede enviar mensaje a los sectores que se requiere mayor de edad
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get("nombre")
        edad = cleaned_data.get("edad")
        departamento= cleaned_data.get("departamento")

        if ((edad < 18) and (departamento=="2" or departamento=="3")):
            msg = f"{nombre}, para colaborar o presentar proyectos debe tener como minimo 18 Años"
            self.add_error('edad',msg)
            raise ValidationError(msg)

class RegistrarUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']