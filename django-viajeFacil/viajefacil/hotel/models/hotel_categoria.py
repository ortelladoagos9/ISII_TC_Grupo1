from django.db import models
from .hotel import Hotel
from .categoria import Categorias

class Hoteles_Categorias(models.Model):
    ID_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    ID_categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ID_hotel} - {self.ID_categoria}"

    class Meta:
        db_table = 'Hoteles_Categorias'
        unique_together = ('ID_hotel', 'ID_categoria')
        verbose_name = "Hoteles_Categorias"
        verbose_name_plural = "Hoteles_Categorias"
