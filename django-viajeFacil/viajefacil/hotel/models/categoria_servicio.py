from django.db import models
from .servicios_hoteles import Servicios_Hoteles
from .servicio_categoria_habitacion import Servicios_Categorias_Habitaciones

class Categorias_Servicios(models.Model):
    ID_servicio_hotel = models.ForeignKey(Servicios_Hoteles, on_delete=models.CASCADE)
    ID_categoria = models.ForeignKey(Servicios_Categorias_Habitaciones, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ID_servicio_hotel} - {self.ID_categoria}"

    class Meta:
        db_table = 'Categorias_Servicios'
        unique_together = ('ID_servicio_hotel', 'ID_categoria')
        verbose_name = "Categoría Servicio"
        verbose_name_plural = "Categorías Servicios"
