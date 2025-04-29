from django.db import models

# SERVICIO
class Servicio(models.Model):
    nombre_servicio = models.CharField(max_length=100)
    descripcion_servicio = models.TextField(max_length=500)

    class Meta:
        ordering = ['-nombre_servicio']

    def __str__(self):
        return self.nombre_servicio

# CATEGORIA
class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=100)
    descripcion_categoria = models.TextField(max_length=500, blank=True)
    capacidad_huesped = models.IntegerField()
    cantidad_hab = models.IntegerField()
    imagen_categoria = models.ImageField(upload_to='habitaciones/%Y/%m/%d', blank=True)
    precio_base_categoria = models.DecimalField(max_digits=20, decimal_places=2)
    estado_categoria = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre_categoria']

    def __str__(self):
        return self.nombre_categoria

# CATEGORIA-SERVICIO
class CategoriaServicio(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('categoria', 'servicio')

    def __str__(self):
        return f"{self.categoria.nombre_categoria} - {self.servicio.nombre_servicio}"

# ESTADO HABITACION
class EstadoHabitacion(models.Model):
    descripcion_estado_habitacion = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Estado de Habitación"
        verbose_name_plural = "Estados de Habitaciones"
        ordering = ['descripcion_estado_habitacion']

    def __str__(self):
        return self.descripcion_estado_habitacion

# ESTADO RESERVA
class EstadoReserva(models.Model):
    descripcion_estado_reserva = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Estado de Reserva'
        verbose_name_plural = 'Estados de Reservas'

    def __str__(self):
        return self.descripcion_estado_reserva

# SERVICIO HOTEL
class ServicioHotel(models.Model):
    nombre_servicio = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Servicio de Hotel'
        verbose_name_plural = 'Servicios de Hotel'
        ordering = ['nombre_servicio']

    def __str__(self):
        return self.nombre_servicio

# PAIS
class Pais(models.Model):
    nombre_pais = models.CharField(max_length=100)

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"

    def __str__(self):
        return self.nombre_pais

# PROVINCIA
class Provincia(models.Model):
    nombre_provincia = models.CharField(max_length=100)
    id_pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='provincias')

    def __str__(self):
        return self.nombre_provincia

# LOCALIDAD
class Localidad(models.Model):
    nombre_localidad = models.CharField(max_length=100)
    id_provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='localidades')

    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"

    def __str__(self):
        return self.nombre_localidad

# DOMICILIO
class Domicilio(models.Model):
    calle_domicilio = models.CharField(max_length=100)
    numero_domicilio = models.CharField(max_length=10)
    id_localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, related_name='domicilios')

    def __str__(self):
        return f"{self.calle_domicilio} {self.numero_domicilio}"

# HOTEL
class Hotel(models.Model):
    nombre_hotel = models.CharField(max_length=100)
    descripcion_hotel = models.TextField()
    cantidad_estrellas_hotel = models.IntegerField()
    imagen_hotel = models.ImageField(upload_to='imagenes_hoteles/', blank=True, null=True)
    id_domicilio = models.OneToOneField(Domicilio, on_delete=models.CASCADE, related_name='hotel')

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hoteles"

    def __str__(self):
        return self.nombre_hotel

#HABITACIONES
class Habitacion(models.Model):
    piso_habitacion = models.IntegerField()
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField()
    id_hoteles = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='habitaciones')
    id_estado_habitacion = models.ForeignKey(EstadoHabitacion, on_delete=models.CASCADE, related_name='habitaciones')
    id_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='habitaciones')

    class Meta:
        verbose_name = "Habitación"
        verbose_name_plural = "Habitaciones"
        ordering = ['id_hoteles', 'piso_habitacion']

    def __str__(self):
        return f"Hotel: {self.id_hoteles.nombre_hotel} - Piso: {self.piso_habitacion}"

#RESERVA HABITACIONES
class ReservaHabitacion(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    estado_reserva = models.ForeignKey(EstadoReserva, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Reserva de Habitación"
        verbose_name_plural = "Reservas de Habitaciones"
        unique_together = ('id_reserva', 'habitacion')

    def __str__(self):
        return f"Reserva {self.id_reserva} - Habitación {self.habitacion.id}"

#RESERVA HOTELES
class ReservaHotel(models.Model):
    cantidad_habitacion = models.IntegerField()
    monto_total_hotel = models.DecimalField(max_digits=20, decimal_places=2)
    id_hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reservas_hoteles')
    id_viajero = models.IntegerField()  # Temporal hasta que tu compañero haga el modelo Viajero

    class Meta:
        verbose_name = "Reserva de Hotel"
        verbose_name_plural = "Reservas de Hoteles"

    def __str__(self):
        return f"Reserva en {self.id_hotel.nombre_hotel} - {self.monto_total_hotel} $"



