from django.shortcuts import render

def index_alojamientos (request):
    return render (request, 'index_alojamientos.html')
