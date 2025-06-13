from django.db import models

class Reservas_Hoteles(models.Model):
    ID_reserva_hotel = models.AutoField(primary_key=True)
    monto_total_hotel = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_reserva = models.DateField(auto_now_add=True)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField()
    ID_viajero = models.ForeignKey('Viajeros', on_delete=models.CASCADE)
    ID_estado_reserva = models.ForeignKey('Estados_Reservas', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Reserva {self.ID_reserva_hotel}"

    class Meta:
        db_table = 'Reservas_Hoteles'
        verbose_name = 'Reserva Hotel'
        verbose_name_plural = 'Reservas Hoteles'
