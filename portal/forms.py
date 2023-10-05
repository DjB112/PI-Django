from django import forms

class ConsultaForm (forms.Form):
    nombre = forms.CharField(
        label="Nombre:",
        max_length=20, 
        required=True, 
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa tu nombre'})
        )
    email = forms.EmailField(
        label="Email:",
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ingresa tu email'})
        )
    edad = forms.IntegerField(
        label="Edad:", 
        required=True, 
        min_value=1, 
        max_value=90, 
        widget=forms.NumberInput(attrs={'class':'form-control w-25','placeholder':'Ingresa tu edad'})
        )
    consulta = forms.CharField(
        label="Consulta:", 
        required=True,
        min_length=12,
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
