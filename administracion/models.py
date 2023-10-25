from collections.abc import Iterable
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.text import slugify

class PersonasManager(models.Manager):
    def cantidad(self):
        return self.count()
    def get_queryset(self):
        return super().get_queryset().filter(estado = True)

class Personas(models.Model):
    id_personas = models.BigAutoField(verbose_name='id_persona',primary_key=True,auto_created=True)
    nombre = models.CharField(verbose_name='nombre', max_length=100, null=False, blank=False)
    apellido = models.CharField(verbose_name='apellido', max_length=150, null=False, blank=False)
    fnac = models.DateField(verbose_name='fnac', null=False)
    dni = models.CharField(verbose_name='dni',null=False,max_length=50,blank=False)
    email= models.EmailField(verbose_name='email', null=False, max_length=100)
    estado=models.BooleanField(verbose_name='estado',default=False,null=False)
    foto_perfil = models.ImageField(upload_to='imagenes/', null=True, verbose_name='foto_perfil')
    # activos = PersonasManager()
    
    def __str__(self):
        return self.nombre

    def delete(self, using=None, keep_parents=False):
        self.foto_perfil.storage.delete(self.perfil_foto.name)  # borrado fisico
        super().delete()
    
    def save(self, *args, **kwargs):
        self.nombre_slug = slugify(f"{self.dni}-{self.nombre}")
        super().save(*args, **kwargs)
    
class Cuerpo(models.Model):
    nombre = models.CharField(verbose_name='nombre',max_length=100,null=False)
    descripcion=models.TextField(verbose_name='descripcion',null=True)
    foto = models.ImageField(upload_to='imagenes/', null=True, verbose_name='foto')
    class Meta:
        abstract = True
        
class Proyecto(Cuerpo):
    class Categorias(models.TextChoices):
        NINGUNA = 'NIG','Ninguna'
        VENTAS = 'VEN', 'Ventas'
        EDUCACION = 'EDU', 'Educacion'
        ENTRETENIMIENTO = 'ENT', 'Entretenimiento'
        MUSICA = 'MUS', 'Musica'
        DISENO = 'DIS', 'Diseño'
        
    id_proyecto =models.BigAutoField(verbose_name='id_proyecto', primary_key=True, auto_created=True)
    categoria = models.CharField(max_length=3, choices=Categorias.choices, default=Categorias.NINGUNA)
    fecha = models.DateField(verbose_name='fecha',null=False,auto_now_add=True)
    personas = models.ForeignKey(Personas,on_delete=models.CASCADE)

class Colaboracion(Cuerpo):
    id_colaboracion = models.BigAutoField(verbose_name='id_colaboracion', primary_key=True, auto_created=True)
    estado = models.BooleanField(verbose_name='estado',null=False, default=False)
    personas = models.ManyToManyField(Personas)

class Comentarios(models.Model):
    id_comentarios=models.BigAutoField(verbose_name='id_comentarios',primary_key=True, auto_created=True)
    persona=models.ManyToManyField(Personas)
    comentario= models.TextField(verbose_name='comentario')