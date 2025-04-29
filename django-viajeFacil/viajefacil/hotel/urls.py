from django.urls import path
from . import views

app_name= 'hotel'

urlpatterns = [
    path('alojamientos/', views.index_alojamientos, name='buscar_alojamientos'),
    path('lista_hoteles/', views.lista_hoteles, name='lista_hoteles')
]