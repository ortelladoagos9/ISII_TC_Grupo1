from django.db import models
from .pais import Pais
from .localidad import Localidad

class Direccion(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE)
    calle = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.calle} {self.numero}, {self.localidad}, {self.pais}"

    class Meta:
        db_table = 'Direcciones'
        verbose_name = "Direccion"
        verbose_name_plural = "Direcciones"
