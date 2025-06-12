from django.db import models
from .viajero import Viajero
from .hotel import Hotel
from .estado_reserva import EstadoReserva

class ReservaHotel(models.Model):
    viajero = models.ForeignKey(Viajero, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    fecha_reserva = models.DateField(auto_now_add=True)
    estado = models.ForeignKey(EstadoReserva, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Reserva {self.id} - {self.viajero} - {self.hotel}"
