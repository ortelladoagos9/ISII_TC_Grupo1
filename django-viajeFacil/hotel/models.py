from django.db import models

class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    descripcion_servicio = models.TextField(max_length=500)

class Meta:
    ordering = ['-nombre_servicio']

def _str_(self):
    return self.nombre_servicio

class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)
    descripcion_categoria = models.TextField(max_length=500, blank=True)
    capacidad_huesped = models.IntegerField()
    cantidad_hab = models.IntegerField()
    imagen_categoria = models.ImageField(upload_to='habitaciones/%Y/%m/%d',
                                        blank=True)
    precio_base_categoria = models.DecimalField(max_digits=20, decimal_places=2)
    estado_categoria = models.BooleanField(default=True)

class Meta:
        ordering = ['nombre_categoria']

def _str_(self):
    return self.nombre_categoria
