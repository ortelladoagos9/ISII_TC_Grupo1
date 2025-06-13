from django.db import models
from .hotel import Hotel
from .servicios_hoteles import Servicios_Hoteles

class Hoteles_Servicios(models.Model):
    ID_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    ID_servicio_hotel = models.ForeignKey(Servicios_Hoteles, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Hoteles_Servicios'
        unique_together = ('ID_hotel', 'ID_servicio_hotel')
        verbose_name = "Hoteles_Servicios"
        verbose_name_plural = "Hoteles_Servicios"

    def __str__(self):
        return f"{self.ID_hotel} - {self.ID_servicio_hotel}"
