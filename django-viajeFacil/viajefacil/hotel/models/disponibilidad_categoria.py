from django.db import models
from .hotel import Hotel
from .categoria import Categorias

class Disponibilidad_Categorias(models.Model):
    ID_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    ID_categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    fecha = models.DateField()
    cantidad_disponible = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.ID_hotel} - {self.ID_categoria} ({self.fecha}): {self.cantidad_disponible}"

    class Meta:
        db_table = 'Disponibilidad_Categorias'
        unique_together = ('ID_hotel', 'ID_categoria', 'fecha')
        verbose_name = "Disponibilidad_Categorias"
        verbose_name_plural = "Disponibilidad_Categorias"
