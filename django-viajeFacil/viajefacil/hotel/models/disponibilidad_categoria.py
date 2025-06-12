from django.db import models
from .hotel import Hotel
from .categoria import Categoria

class DisponibilidadCategoria(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad_disponible = models.PositiveIntegerField()

    class Meta:
        unique_together = ('hotel', 'categoria', 'fecha')

    def __str__(self):
        return f"{self.hotel} - {self.categoria} ({self.fecha}): {self.cantidad_disponible}"
