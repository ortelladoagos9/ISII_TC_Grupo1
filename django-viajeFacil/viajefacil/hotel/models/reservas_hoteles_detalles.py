from django.db import models

class Reservas_Hoteles_Detalles(models.Model):
    ID_reserva_hotel_detalle = models.AutoField(primary_key=True)
    cantidad_habitaciones = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=12, decimal_places=2)
    ID_categoria = models.ForeignKey('Categorias', on_delete=models.CASCADE)
    ID_reserva_hotel = models.ForeignKey('Reservas_Hoteles', on_delete=models.CASCADE)

    def __str__(self):
        return f"Detalle {self.ID_reserva_hotel_detalle}"

    class Meta:
        db_table = 'Reservas_Hoteles_Detalles'
        verbose_name = 'Detalle Reserva Hotel'
        verbose_name_plural = 'Detalles Reservas Hoteles'
