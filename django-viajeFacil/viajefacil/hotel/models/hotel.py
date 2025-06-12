from django.db import models
from .direccion import Direccion

class Hotel(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre
