from django import forms
from django.forms import ValidationError
import re
from administracion.models import Personas, Colaboracion, Comentarios, Cuerpo, Proyecto

class PersonasForm(forms.ModelForm):
    class Meta:
        model = Personas
        exclude =['id_personas']