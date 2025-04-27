from django.contrib import admin
from .models import Servicio
from .models import Categoria

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display=['nombre_servicio', 'descripcion_servicio']
@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre_categoria', 'descripcion_categoria', 'capacidad_huesped', 'cantidad_hab', 'imagen_categoria', 'precio_base_categoria', 'estado_categoria']
    list_filter = ['cantidad_hab', 'estado_categoria']
    