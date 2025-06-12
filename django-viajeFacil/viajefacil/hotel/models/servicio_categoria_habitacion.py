from django.db import models

class ServicioCategoriaHabitacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servicio Categoría Habitación"
        verbose_name_plural = "Servicios Categorías Habitaciones"
