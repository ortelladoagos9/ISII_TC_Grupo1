from django.shortcuts import render
from .models import Hotel
from .models import Categoria

def index_alojamientos (request):
    return render (request, 'index_alojamientos.html')

def lista_hoteles (request):
    return render (request, 'lista_hoteles.html')

def lista_hoteles(request):
    hoteles = Hotel.objects.all().prefetch_related('habitaciones__categoria')
    return render(request, 'lista_hoteles.html', {'hoteles': hoteles})

