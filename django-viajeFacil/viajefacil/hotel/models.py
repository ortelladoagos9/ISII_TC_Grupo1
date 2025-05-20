from django.db import models

# =============================
# Ubicación: País, Provincia, Localidad, Dirección
# =============================

class Pais(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "País"
        verbose_name_plural = "Países"


class Provincia(models.Model):
    nombre = models.CharField(max_length=100)
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name='provincias')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"


class Localidad(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='localidades')

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Localidad"
        verbose_name_plural = "Localidades"


class Direccion(models.Model):
    calle = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    cod_postal = models.CharField(max_length=10)
    localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, related_name='direcciones')

    def __str__(self):
        return f"{self.calle} {self.numero}, CP {self.cod_postal}"

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"


# =============================
# Viajero
# =============================

class Viajero(models.Model):
    identificacion = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    fecha_nacimiento = models.DateField()
    clave = models.CharField(max_length=128)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

    class Meta:
        verbose_name = "Viajero"
        verbose_name_plural = "Viajeros"


# =============================
# Hotel y Categoría
# =============================

class Hotel(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estrellas = models.PositiveSmallIntegerField()
    imagen = models.ImageField(upload_to='hoteles/', null=True, blank=True)
    direccion = models.ForeignKey(Direccion, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hoteles"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    capacidad = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    precio = models.FloatField(default=0.00)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


class HotelCategoria(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='categorias_hotel')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Hotel Categoría"
        verbose_name_plural = "Hoteles Categorías"
        unique_together = ('hotel', 'categoria')

    def __str__(self):
        return f"{self.hotel} - {self.categoria}"


# =============================
# Servicios
# =============================

class ServicioHotel(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servicio Hotel"
        verbose_name_plural = "Servicios Hoteles"

class HotelServicio(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    servicio = models.ForeignKey(ServicioHotel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Hotel Servicio"
        verbose_name_plural = "Hoteles Servicios"
        unique_together = ('hotel', 'servicio')

    def __str__(self):
        return f"{self.hotel} - {self.servicio}"


class ServicioCategoriaHabitacion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Servicio Categoría Habitación"
        verbose_name_plural = "Servicios Categorías Habitaciones"


class CategoriaServicio(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    servicio = models.ForeignKey(ServicioCategoriaHabitacion, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Categoría Servicio"
        verbose_name_plural = "Categorías Servicio"
        unique_together = ('categoria', 'servicio')

    def __str__(self):
        return f"{self.categoria} - {self.servicio}"


# =============================
# Disponibilidad
# =============================

class DisponibilidadCategoria(models.Model):
    fecha = models.DateField()
    capacidad_disponible = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='disponibilidades')

    def __str__(self):
        return f"{self.categoria.nombre} - {self.fecha} ({self.capacidad_disponible})"

    class Meta:
        verbose_name = "Disponibilidad Categoría"
        verbose_name_plural = "Disponibilidad Categorías"


# =============================
# Reservas
# =============================

class EstadoReserva(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion

    class Meta:
        verbose_name = "Estado Reserva"
        verbose_name_plural = "Estados Reservas"


class ReservaHotel(models.Model):
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_reserva = models.DateField()
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField()
    viajero = models.ForeignKey(Viajero, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoReserva, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reserva {self.id} - {self.viajero}"

    class Meta:
        verbose_name = "Reserva Hotel"
        verbose_name_plural = "Reservas Hoteles"


class ReservaHotelDetalle(models.Model):
    cantidad_habitaciones = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    reserva = models.ForeignKey(ReservaHotel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reserva} - {self.categoria} - {self.cantidad_habitaciones} hab."

    def save(self, *args, **kwargs):
        self.sub_total = self.precio_unitario * self.cantidad_habitaciones
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Reserva Hotel Detalle"
        verbose_name_plural = "Reservas Hoteles Detalles"