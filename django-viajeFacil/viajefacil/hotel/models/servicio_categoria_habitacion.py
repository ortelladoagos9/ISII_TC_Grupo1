from django.db import models
from .servicios_hoteles import Servicios_Hoteles
from .categoria import Categorias

class Servicios_Categorias_Habitaciones(models.Model):
    ID_servicio_hotel = models.ForeignKey(Servicios_Hoteles, on_delete=models.CASCADE)
    ID_categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ID_servicio_hotel} - {self.ID_categoria}"

    class Meta:
        db_table = 'Servicios_Categorias_Habitaciones'
        unique_together = ('ID_servicio_hotel', 'ID_categoria')
        verbose_name = 'Servicio por Categoría de Habitación'
        verbose_name_plural = 'Servicios por Categorías de Habitaciones'
