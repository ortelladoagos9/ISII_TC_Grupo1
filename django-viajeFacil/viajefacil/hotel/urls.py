from django.urls import path
from . import views

app_name= 'hotel'

urlpatterns = [
    path('alojamientos/', views.index_alojamientos, name='buscar_alojamientos'),
    path('lista_hoteles/', views.lista_hoteles, name='lista_hoteles'),
    path('api/destinos/', views.obtener_destinos, name='api_destinos'),  
    path('ajax/buscar-destinos/', views.buscar_destinos, name='ajax_buscar_destinos'),
    path('alojamientos/por-destino/', views.hoteles_por_destino, name='hoteles_por_destino'),
    path('detalle/<int:id>/', views.detalle_hotel, name='detalle_hotel'),
    path('seleccionar-categoria/', views.seleccionar_categoria, name='seleccionar_categoria'),
    path('reserva/', views.detalle_reserva, name='detalle_reserva'),
    path('guardar-viajero/', views.guardar_datos_viajero, name='guardar_datos_viajero'),

    
]