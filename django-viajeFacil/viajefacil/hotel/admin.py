from django.contrib import admin
from .models import (
    Pais, Provincia, Localidad, Direccion,
    Viajero,
    Hotel, Categoria, HotelCategoria,
    ServicioHotel, HotelServicio,
    ServicioCategoriaHabitacion, CategoriaServicio,
    DisponibilidadCategoria,
    EstadoReserva, ReservaHotel, ReservaHotelDetalle
)

# ========== UBICACIÓN ==========
@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'pais']
    list_filter = ['pais']
    search_fields = ['nombre']


@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'provincia']
    list_filter = ['provincia']
    search_fields = ['nombre']


@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ['id', 'calle', 'numero', 'cod_postal', 'localidad']
    search_fields = ['calle', 'numero', 'cod_postal']


# ========== VIAJERO ==========
@admin.register(Viajero)
class ViajeroAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'apellido', 'email', 'telefono']
    search_fields = ['nombre', 'apellido', 'email']


# ========== HOTEL & CATEGORÍA ==========
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'estrellas', 'direccion']
    search_fields = ['nombre']
    list_filter = ['estrellas']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'capacidad', 'precio']
    search_fields = ['nombre']
    list_filter = ['capacidad']


@admin.register(HotelCategoria)
class HotelCategoriaAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'categoria']
    list_filter = ['hotel', 'categoria']
    search_fields = ['hotel__nombre', 'categoria__nombre']


# ========== SERVICIOS ==========
@admin.register(ServicioHotel)
class ServicioHotelAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


@admin.register(HotelServicio)
class HotelServicioAdmin(admin.ModelAdmin):
    list_display = ['hotel', 'servicio']
    list_filter = ['hotel', 'servicio']


@admin.register(ServicioCategoriaHabitacion)
class ServicioCategoriaHabitacionAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']


@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'servicio']
    list_filter = ['categoria', 'servicio']


# ========== DISPONIBILIDAD ==========
@admin.register(DisponibilidadCategoria)
class DisponibilidadCategoriaAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'fecha', 'capacidad_disponible']
    list_filter = ['categoria', 'fecha']


# ========== RESERVAS ==========
@admin.register(EstadoReserva)
class EstadoReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'descripcion']
    search_fields = ['descripcion']


@admin.register(ReservaHotel)
class ReservaHotelAdmin(admin.ModelAdmin):
    list_display = ['id', 'viajero', 'fecha_reserva', 'fecha_ingreso', 'fecha_egreso', 'estado', 'monto_total']
    list_filter = ['estado', 'fecha_reserva']
    search_fields = ['viajero__nombre', 'viajero__apellido']


@admin.register(ReservaHotelDetalle)
class ReservaHotelDetalleAdmin(admin.ModelAdmin):
    list_display = ['reserva', 'categoria', 'cantidad_habitaciones', 'precio_unitario', 'sub_total']
    list_filter = ['categoria']
