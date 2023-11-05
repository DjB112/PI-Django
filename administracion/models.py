from collections.abc import Iterable
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.text import slugify

class DisenadoresManager(models.Manager):
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
    estado=models.BooleanField(verbose_name='Diseñador',default=False,null=False)
    foto_perfil = models.ImageField(upload_to='imagenes/perfiles/', null=True, blank=True, default="", verbose_name='foto_perfil')
    objects = models.Manager()
    disenadores = DisenadoresManager()
    
    def __str__(self):
        return self.nombre
    
    def save(self, *args, **kwargs):
        self.nombre_slug = slugify(f"{self.dni}-{self.nombre}")
        super().save(*args, **kwargs)
    
    def delete(self, using=None, keep_parents=False):
        self.foto_perfil.storage.delete(self.foto_perfil.name)  # borrado fisico
        super().delete()
    
    def obtener_baja_url(self):
        return reverse_lazy('persona_baja', args=[self.id_personas])
    
    def obtener_modificacion_url(self):
        return reverse_lazy('persona_modificacion', args=[self.id_personas])
    
    class Meta:
        verbose_name_plural = "Personas"
    
class Cuerpo(models.Model):
    nombre = models.CharField(verbose_name='nombre',max_length=100,null=False)
    descripcion=models.CharField(verbose_name='descripcion',null=False, max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de modificación")
    estado = models.BooleanField(verbose_name='Estado Activo',null=False, default=False)
    class Meta:
        abstract = True

class CategoriaProyectos(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    estado = models.BooleanField(verbose_name='Categoria Activa',default=False)
    objects = models.Manager()

    def __str__(self):
        return self.nombre

    def save(self):
        return super().save()
    
    def obtener_baja_url(self):
        return reverse_lazy('categoriasproyecto_baja', args=[self.id])
    
    def obtener_modificacion_url(self):
        return reverse_lazy('categoriasproyecto_editar', args=[self.id])
    # def delete(self): se utiliza si queremos sobreescribir el delete con soft_delete
    #     self.soft_delete()   
    class Meta:
        verbose_name_plural = "CategoriaProyectos"
            
class CategoriaColaboraciones(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre')
    estado = models.BooleanField(verbose_name='Categoria Activa',default=False)

    def __str__(self):
        return self.nombre

    def save(self):
        super().save()
    
    def obtener_baja_url(self):
        return reverse_lazy('categoriascolaboracion_baja', args=[self.id])
    
    def obtener_modificacion_url(self):
        return reverse_lazy('categoriascolaboracion_editar', args=[self.id])

    class Meta:
        verbose_name_plural = "CategoriaColaboraciones"
                 
class Proyecto(Cuerpo):        
    id_proyecto =models.BigAutoField(verbose_name='id_proyecto', primary_key=True, auto_created=True)
    categoria = models.ForeignKey(CategoriaProyectos, on_delete=models.CASCADE)
    personas = models.ForeignKey(Personas,on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='imagenes/proyectos/', null=True, verbose_name='foto')
    
    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

    def delete(self, using=None, keep_parents=False):
        self.foto.storage.delete(self.foto.name)  # borrado fisico
        super().delete()
    
    def obtener_baja_url(self):
        return reverse_lazy('proyecto_baja', args=[self.id_proyecto])

    def obtener_modificacion_url(self):
        return reverse_lazy('proyecto_editar', args=[self.id_proyecto])

    class Meta:
        verbose_name_plural = "Proyectos"

# class ComentarioProyecto(models.Model):
#     id_comentario=models.BigAutoField(verbose_name='id_comentario', primary_key=True, auto_created=True)
#     id_persona= models.ForeignKey(Personas, on_delete= models.SET_NULL)
#     comentario = models.CharField(verbose_name='comentario',null=True,blank=False, max_length=250)
#     fecha = models.DateTimeField(auto_now=True, verbose_name="Fecha")
#     visible = models.BooleanField(verbose_name='Visible',default=True)
    
class Colaboracion(Cuerpo):
    id_colaboracion = models.BigAutoField(verbose_name='id_colaboracion', primary_key=True, auto_created=True)
    categoria = models.ForeignKey(CategoriaColaboraciones, on_delete=models.CASCADE)
    personas = models.ManyToManyField(Personas, through='Participaciones')
    foto = models.ImageField(upload_to='imagenes/colaboraciones', null=True, verbose_name='foto')

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"
    
    def obtener_baja_url(self):
        return reverse_lazy('colaboracion_baja', args=[self.id_colaboracion])

    def obtener_modificacion_url(self):
        return reverse_lazy('colaboracion_editar', args=[self.id_colaboracion])

    class Meta:
        verbose_name_plural = "Colaboraciones"

class Participaciones(models.Model):
    fecha_participacion = models.DateField(auto_now_add=True, verbose_name='Fecha de creacion')
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    colaboracion = models.ForeignKey(Colaboracion, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.colaboracion.nombre} - {self.colaboracion.categoria}"
    
    def obtener_baja_url(self):
        return reverse_lazy('participacion_baja', args=[self.id])

    def obtener_modificacion_url(self):
        return reverse_lazy('participacion_modificacion', args=[self.id])

    class Meta:
        verbose_name_plural = "Participaciones"
    
class Comentarios(models.Model):
    id_comentarios=models.BigAutoField(verbose_name='id_comentarios',primary_key=True, auto_created=True)
    persona=models.ManyToManyField(Personas)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    comentario= models.TextField(verbose_name='comentario')

    class Meta:
        verbose_name_plural = "Comentarios"