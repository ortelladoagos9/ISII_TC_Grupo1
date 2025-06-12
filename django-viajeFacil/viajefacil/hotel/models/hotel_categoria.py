# hotel/models/hotel_categoria.py
from django.db import models
from .hotel import Hotel
from .categoria import Categoria

class HotelCategoria(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hotel', 'categoria')

    def __str__(self):
        return f"{self.hotel} - {self.categoria}"
