from django.db import models

class Categorias(models.Model):
    ID_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50)
    descripcion_categoria = models.TextField(null=True, blank=True)
    capacidad_categoria = models.IntegerField()
    imagen_categoria = models.ImageField(upload_to='imagenes_categorias/', null=True, blank=True)

    def __str__(self):
        return self.nombre_categoria

    class Meta:
        db_table = 'Categorias'
        verbose_name = "Categorías"
        verbose_name_plural = "Categorías"
