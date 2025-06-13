from django.db import models
from .pais import Pais

class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Provincias'

    def __str__(self):
        return f"{self.nombre}, {self.pais.nombre}"
