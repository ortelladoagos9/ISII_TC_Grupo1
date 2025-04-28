from django.contrib import admin
from .models import Servicio, Categoria, CategoriaServicio, EstadoHabitacion, EstadoReserva, ServicioHotel, Pais, Provincia, Localidad, Domicilio, Hotel, Habitacion, ReservaHabitacion, ReservaHotel

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre_servicio', 'descripcion_servicio']
    search_fields = ['nombre_servicio']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre_categoria', 'descripcion_categoria', 'capacidad_huesped', 'cantidad_hab', 'preview_imagen', 'precio_base_categoria', 'estado_categoria']
    list_filter = ['cantidad_hab', 'estado_categoria']
    search_fields = ['nombre_categoria']
    readonly_fields = ['preview_imagen']

    def preview_imagen(self, obj):
        if obj.imagen_categoria:
            return f'<img src="{obj.imagen_categoria.url}" width="100" height="60" />'
        return "(No imagen)"
    preview_imagen.allow_tags = True
    preview_imagen.short_description = 'Vista previa'

@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ['categoria', 'servicio']
    search_fields = ['categoria__nombre_categoria', 'servicio__nombre_servicio']

@admin.register(EstadoHabitacion)
class EstadoHabitacionAdmin(admin.ModelAdmin):
    list_display = ['descripcion_estado_habitacion']
    search_fields = ['descripcion_estado_habitacion']

@admin.register(EstadoReserva)
class EstadoReservaAdmin(admin.ModelAdmin):
    list_display = ['descripcion_estado_reserva']
    search_fields = ['descripcion_estado_reserva']

@admin.register(ServicioHotel)
class ServicioHotelAdmin(admin.ModelAdmin):
    list_display = ['nombre_servicio']
    search_fields = ['nombre_servicio']

@admin.register(Pais)
class PaisAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_pais')
    search_fields = ('nombre_pais',)

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_provincia', 'id_pais')
    search_fields = ('nombre_provincia',)
    list_filter = ('id_pais',)

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_localidad', 'id_provincia')
    search_fields = ('nombre_localidad',)
    list_filter = ('id_provincia',)

@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('id', 'calle_domicilio', 'numero_domicilio', 'id_localidad')
    search_fields = ('calle_domicilio',)
    list_filter = ('id_localidad',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre_hotel', 'cantidad_estrellas_hotel', 'id_domicilio')
    search_fields = ('nombre_hotel',)
    list_filter = ('cantidad_estrellas_hotel',)

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'piso_habitacion', 'fecha_ingreso', 'fecha_egreso', 'id_hoteles', 'id_estado_habitacion', 'id_categoria')
    list_filter = ('id_hoteles', 'id_estado_habitacion', 'id_categoria')
    search_fields = ('id_hoteles__nombre_hotel', 'piso_habitacion')

@admin.register(ReservaHabitacion)
class ReservaHabitacionAdmin(admin.ModelAdmin):
    list_display = ('id_reserva', 'habitacion', 'fecha_reserva', 'estado_reserva')
    list_filter = ('estado_reserva', 'fecha_reserva')
    search_fields = ('id_reserva', 'habitacion__id')

@admin.register(ReservaHotel)
class ReservaHotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_hotel', 'id_viajero', 'cantidad_habitacion', 'monto_total_hotel')
    list_filter = ('id_hotel',)
    search_fields = ('id', 'id_hotel__nombre_hotel')




