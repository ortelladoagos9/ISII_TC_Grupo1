from django.shortcuts import render
from django.http import JsonResponse
from .models import Hotel, Localidad, Hoteles_Categorias 

def index_alojamientos (request):
    return render (request, 'index_alojamientos.html')

def lista_hoteles(request):
    hoteles = Hotel.objects.prefetch_related('categorias_hotel__categoria')  # prefetch de relación M2M
    return render(request, 'lista_hoteles.html', {'hoteles': hoteles})

def obtener_destinos(request):
    localidades = Localidad.objects.select_related('provincia__pais').all()
    destinos = []

    for loc in localidades:
        destinos.append({
            'localidad': loc.nombre,
            'provincia': loc.provincia.nombre,
            'pais': loc.provincia.pais.nombre,
        })

    return JsonResponse(destinos, safe=False)
