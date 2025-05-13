from django.shortcuts import render
from .models import Hotel
from .models import Categoria
from django.http import JsonResponse
from .models import Localidad

def index_alojamientos (request):
    return render (request, 'index_alojamientos.html')

def lista_hoteles (request):
    return render (request, 'lista_hoteles.html')

def lista_hoteles(request):
    hoteles = Hotel.objects.all().prefetch_related('habitaciones__categoria')
    return render(request, 'lista_hoteles.html', {'hoteles': hoteles})

def obtener_destinos(request):
    localidades = Localidad.objects.select_related('id_provincia__id_pais').all()
    destinos = []

    for loc in localidades:
        destinos.append({
            'localidad': loc.nombre_localidad,
            'provincia': loc.id_provincia.nombre_provincia,
            'pais': loc.id_provincia.id_pais.nombre_pais,
        })

    return JsonResponse(destinos, safe=False)
