# hotel/models/categoria.py
from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre
