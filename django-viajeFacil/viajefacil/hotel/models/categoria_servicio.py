from django.db import models
from .servicio_hotel import ServicioHotel
from .servicio_categoria_habitacion import ServicioCategoriaHabitacion

class CategoriaServicio(models.Model):
    servicio = models.ForeignKey(ServicioHotel, on_delete=models.CASCADE)
    categoria = models.ForeignKey(ServicioCategoriaHabitacion, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('servicio', 'categoria')

    def __str__(self):
        return f"{self.servicio} - {self.categoria}"
