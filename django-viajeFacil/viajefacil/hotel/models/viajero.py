from django.db import models

class Viajeros(models.Model):
    identificacion = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    fecha_nacimiento = models.DateField()
    clave = models.CharField(max_length=128)
    ID_direccion = models.ForeignKey("hotel.Direccion", on_delete=models.CASCADE)


    class Meta:
        db_table = 'Viajeros'
        verbose_name = "Viajero"
        verbose_name_plural = "Viajeros"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
