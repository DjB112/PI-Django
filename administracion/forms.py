from django import forms
from django.forms import ValidationError
import re
from administracion.models import Novedades, Personas,Participaciones, CategoriaProyectos,CategoriaColaboraciones, Colaboracion, Comentarios, Cuerpo, Proyecto

def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('El nombre no puede contener números. %(valor)s',
                              code='Error1',
                              params={'valor': value})

class NovedadesForm(forms.ModelForm):

    class Meta:    
        model = Novedades
        fields = ("titulo", "mensaje",'estado','contenido','imagen')
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Titulo de Novedad'}),
            'mensaje': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Mensaje Breve'}),
            'contenido': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Ingrese aqui el texto largo'}),
        }

class PersonasForm(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre:',
        required=True,
        validators=(solo_caracteres,),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese solo texto'})
    )
    apellido = forms.CharField(
        label='Nombre:',
        required=True,
        validators=(solo_caracteres,),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese solo texto'})
    )
    class Meta:    
        model = Personas
        fields = ("nombre", "apellido",'fnac','dni','email','estado','foto_perfil')
        widgets = {
            'fnac': forms.DateInput(attrs={'class':'form-control','placeholder':'DD/MM/AAAA'}),
            'dni': forms.NumberInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }
        
class CategoriaFormProyectos(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre:',
        required=True,
        validators=(solo_caracteres,),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese solo texto'})
    )
    class Meta:
        model = CategoriaProyectos
        fields = ['nombre','estado']
    
    def clean_nombre(self):
        nombre = self.cleaned_data['nombre']
        if  nombre.upper() =="DJANGO":
            raise ValidationError("QUE HACES?? NO PUEDE HABER MAS DJANGO")
        return nombre


class CategoriaFormColaboraciones(forms.ModelForm):
    nombre = forms.CharField(
        label='Nombre:',
        required=True,
        validators=(solo_caracteres,),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese solo texto'})
    )
    class Meta:
        model = CategoriaColaboraciones
        fields = ['nombre','estado']

class ProyectosForm(forms.ModelForm):

    class Meta:    
        model = Proyecto
        fields = ['nombre', 'descripcion','estado','categoria','personas','foto',]
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control','rows':10}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'personas': forms.Select(attrs={'class':'form-control'})
            
        }
        
class ColaboracionForm(forms.ModelForm):

    class Meta:    
        model = Colaboracion
        fields = ['nombre', 'descripcion','estado','categoria','personas','foto']
        widgets = {
            'nombre': forms.TextInput(attrs={'class':'form-control'}),
            'descripcion': forms.Textarea(attrs={'class':'form-control','rows':10}),
            'categoria': forms.Select(attrs={'class':'form-control'}),
            'personas': forms.SelectMultiple(attrs={'class':'form-control'})
            
        }
        
class ParticipacionesForm(forms.ModelForm):

    class Meta:    
        model = Participaciones
        fields = ('__all__')

class ComentariosForm(forms.ModelForm):

    class Meta:    
        model = Comentarios
        fields = ['comentario','estado']
        widgets = {
            'comentario': forms.Textarea(attrs={'class':'form-control','rows':10}),
        }