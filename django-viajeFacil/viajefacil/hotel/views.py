from django.shortcuts import render

def index_alojamientos (request):
    return render (request, 'index_alojamientos.html')

def lista_hoteles (request):
    return render (request, 'lista_hoteles.html')
