from collections.abc import Iterable
from django.db import models
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.models import User

class NovedadesManager(models.Manager):
    def cantidad(self):
        return self.count()
    def get_queryset(self):
        return super().get_queryset().filter(estado = True)
    
class Novedades(models.Model):
    id_novedad = models.BigAutoField(verbose_name='id_novedad',primary_key=True,auto_created=True)
    titulo = models.CharField(verbose_name='Titulo', max_length=200, null=False, blank=False)
    mensaje = models.CharField(verbose_name='Mensaje Corto', max_length=250, null=False, blank=False)
    estado = models.BooleanField(verbose_name='Estado Activo',default=False,null=False)
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    contenido = models.TextField(verbose_name="Contenido",null=False,blank=False)
    imagen =  models.ImageField(upload_to='imagenes/novedades/', null=True, blank=True, default="", verbose_name='Imagen Novedad')
    objects = models.Manager()
    novedades = NovedadesManager()
    
    def __str__(self):
        return self.titulo
    
    def save(self, *args, **kwargs):
        self.titulo_slug = slugify(f"{self.id_novedad}-{self.fecha}")
        super().save(*args, **kwargs)
    
    def SetInactivos(self):
        self.estado =False
        self.save()
    
    def SetActivos(self):
        self.estado =True
        self.save()
    
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)  # borrado fisico
        super().delete()
    
    def obtener_baja_url(self):
        return reverse_lazy('novedad_baja', args=[self.id_novedad])
    
    def obtener_modificacion_url(self):
        return reverse_lazy('novedad_editar', args=[self.id_novedad])
       
    class Meta:
        ordering = ["-fecha"]
        verbose_name_plural = "Novedades"
        
class DisenadoresManager(models.Manager):
    def cantidad(self):
        return self.count()
    def get_queryset(self):
        return super().get_queryset().filter(estado = True)

class Personas(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_personas = models.BigAutoField(verbose_name='id_persona',primary_key=True,auto_created=True)
    nombre = models.CharField(verbose_name='nombre', max_length=100, null=False, blank=False)
    apellido = models.CharField(verbose_name='apellido', max_length=150, null=False, blank=False)
    fnac = models.DateField(verbose_name='fnac', null=False)
    dni = models.CharField(verbose_name='dni',null=False,max_length=50,blank=False)
    email= models.EmailField(verbose_name='email', null=False, max_length=100)
    estado=models.BooleanField(verbose_name='Diseñador',default=False,null=False)
    foto_perfil = models.ImageField(upload_to='imagenes/perfiles/', default="avatar.jpg" ,null=True, blank=True, verbose_name='foto_perfil')
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
    descripcion=models.TextField(verbose_name='descripcion',null=False, max_length=255)
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

    def SetInactivos(self):
        self.estado =False
        self.save()
    
    def SetActivos(self):
        self.estado =True
        self.save()
    
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

    def SetInactivos(self):
        self.estado =False
        self.save()
    
    def SetActivos(self):
        self.estado =True
        self.save()
    
    def obtener_baja_url(self):
        return reverse_lazy('categoriascolaboracion_baja', args=[self.id])
    
    def obtener_modificacion_url(self):
        return reverse_lazy('categoriascolaboracion_editar', args=[self.id])

    class Meta:
        verbose_name_plural = "CategoriaColaboraciones"

class ProyectoManager(models.Manager):
    def cantidad(self):
        return self.count()
    def get_queryset(self):
        return super().get_queryset().filter(estado = True)
                 
class Proyecto(Cuerpo):        
    id_proyecto =models.BigAutoField(verbose_name='id_proyecto', primary_key=True, auto_created=True)
    categoria = models.ForeignKey(CategoriaProyectos, on_delete=models.CASCADE)
    personas = models.ForeignKey(Personas,on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='imagenes/proyectos/', null=True, verbose_name='foto')
    objects = models.Manager()
    activos = ProyectoManager()
       
    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

    def delete(self, using=None, keep_parents=False):
        self.foto.storage.delete(self.foto.name)  # borrado fisico
        super().delete()
    
    def SetInactivos(self):
        self.estado =False
        self.save()
    
    def SetActivos(self):
        self.estado =True
        self.save()
    
    def obtener_baja_url(self):
        return reverse_lazy('proyecto_baja', args=[self.id_proyecto])

    def obtener_modificacion_url(self):
        return reverse_lazy('proyecto_editar', args=[self.id_proyecto])
    
    def obtener_comentarios_url(self):
        return reverse_lazy('comentarios_proyecto', args=[self.id_proyecto])

    def misproyectos_baja_url(self):
        return reverse_lazy('misproyectos_baja', args=[self.id_proyecto])

    def misproyectos_modificacion_url(self):
        return reverse_lazy('misproyectos_editar', args=[self.id_proyecto])
    
    def misproyectos_comentarios_url(self):
        return reverse_lazy('comentarios_proyecto', args=[self.id_proyecto])

    class Meta:
        verbose_name_plural = "Proyectos"
        ordering = ["-fecha_creacion"]
    
class ColaboracionManager(models.Manager):
    def cantidad(self):
        return self.count()
    
    def get_queryset(self):
        return super().get_queryset().filter(estado = True)    

class Colaboracion(Cuerpo):
    id_colaboracion = models.BigAutoField(verbose_name='id_colaboracion', primary_key=True, auto_created=True)
    categoria = models.ForeignKey(CategoriaColaboraciones, on_delete=models.CASCADE)
    personas = models.ManyToManyField(Personas, through='Participaciones')
    foto = models.ImageField(upload_to='imagenes/colaboraciones', null=True, verbose_name='foto')
    objects = models.Manager()
    ultimacolaboracion = ColaboracionManager()    

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"
    
    def obtener_baja_url(self):
        return reverse_lazy('colaboracion_baja', args=[self.id_colaboracion])

    def obtener_modificacion_url(self):
        return reverse_lazy('colaboracion_editar', args=[self.id_colaboracion])

    def miscolaboraciones_baja_url(self):
        return reverse_lazy('miscolaboraciones_baja', args=[self.id_colaboracion])

    def miscolaboraciones_modificacion_url(self):
        return reverse_lazy('miscolaboraciones_editar', args=[self.id_colaboracion])
    
    class Meta:
        verbose_name_plural = "Colaboraciones"
        ordering = ["-fecha_creacion"]

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
    
class ComentariosManager(models.Manager):
    def cantidad(self):
        return self.count()
    def get_queryset(self):
        return super().get_queryset().filter(estado = True)

class Comentarios(models.Model):
    class Estado(models.TextChoices):
        PROYECTO = 'PRO', 'Proyecto'
        COLABORACION = 'COL', 'Colaboracion'
    id_comentarios = models.BigAutoField(verbose_name='id_comentarios',primary_key=True, auto_created=True)
    nro_proyecto = models.ForeignKey(Proyecto, on_delete=models.SET_NULL,null=True)
    id_persona = models.ForeignKey(Personas,on_delete=models.SET_NULL,null=True)
    tipo=models.CharField(max_length=3, choices=Estado.choices, default=Estado.PROYECTO)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    comentario= models.TextField(verbose_name='comentario')
    estado= models.BooleanField(verbose_name='Visible',default=True)
    objects = models.Manager()
    novedades = ComentariosManager()
      
    def obtener_comentarios_url(self):
        return reverse_lazy('comentarios_proyecto', args=[self.id_comentarios])
    
    def obtener_modificacion_com(self):
        return reverse_lazy('comentario_editar', args=[self.id_comentarios])

    def obtener_eliminar_com(self):
        return reverse_lazy('comentario_eliminar', args=[self.id_comentarios])
    
    class Meta:
        verbose_name_plural = "Comentarios"