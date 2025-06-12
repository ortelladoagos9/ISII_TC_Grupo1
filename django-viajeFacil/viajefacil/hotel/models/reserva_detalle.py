from django.db import models

class ReservaHotelDetalle(models.Model):
    reserva = models.ForeignKey("hotel.ReservaHotel", on_delete=models.CASCADE)    
    categoria = models.ForeignKey("hotel.Categoria", on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.reserva} - {self.categoria} del {self.fecha_inicio} al {self.fecha_fin}"
