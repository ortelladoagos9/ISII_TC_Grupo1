from django.db import models

class Servicios_Hoteles(models.Model):
    ID_servicio_hotel = models.AutoField(primary_key=True)
    nombre_servicio = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_servicio

    class Meta:
        db_table = 'Servicios_Hoteles'
        verbose_name = 'Servicio Hotel'
        verbose_name_plural = 'Servicios Hoteles'