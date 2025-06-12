from django.db import models
from .hotel import Hotel
from .servicio_hotel import ServicioHotel

class HotelServicio(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    servicio = models.ForeignKey(ServicioHotel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hotel', 'servicio')

    def __str__(self):
        return f"{self.hotel} - {self.servicio}"
