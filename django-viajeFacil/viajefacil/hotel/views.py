from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Hotel, Localidad, Hoteles_Categorias
from django.db import connection
from datetime import datetime
import locale
import math
from .utils import obtenerHoteles
from .utils import buscarHotel
from .utils import mostrarHabitacionesHotel
from .utils import mostrarServiciosHotel
from .utils import mostrarServiciosCategorias
from .utils import buscarHotelPorId
from .utils import buscarCategoriaPorId
from .utils import insertarViajero

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
            'localidad': loc.nombre_localidad,
            'provincia': loc.provincia,
            'pais': loc.provincia.pais.nombre_pais,
        })

    return JsonResponse(destinos, safe=False)

def index_alojamientos(request):
    hoteles_lista = obtenerHoteles()
    paginator = Paginator(hoteles_lista, 2)  #2 hoteles por página

    page_number = request.GET.get('page')  # página actual
    hoteles = paginator.get_page(page_number)

    return render(request, 'index_alojamientos.html', {
        'hoteles': hoteles
    })

def buscar_destinos(request):
    termino = request.GET.get('term', '')

    resultados = []
    if termino:
        with connection.cursor() as cursor:
            cursor.execute("EXEC busquedaDestinos %s", [termino])
            for row in cursor.fetchall():
                resultados.append({
                    'destino': row[0],  # texto visible
                    'tipo': row[1],     # 'provincia' o 'localidad'
                    'id': row[2]        # ID
                })

    return JsonResponse(resultados, safe=False)

def alojamientos(request):
    tipo = request.GET.get("tipo")
    id_origen = request.GET.get("id")

    hoteles = []
    if tipo and id_origen:
        try:
            hoteles = buscarHotel(id_origen,tipo)
        except Exception as e:
            print(f"Error al buscar hoteles: {e}")
            hoteles = []

    paginator = Paginator(hoteles, 3)
    page_number = request.GET.get('page')
    hoteles_paginados = paginator.get_page(page_number)

    return render(request, 'index_alojamientos.html', {
        'hoteles': hoteles_paginados
    })

def hoteles_por_destino(request):

    # Guardamos los datos de búsqueda en sesión
    request.session['busqueda'] = {
    'fecha_ingreso': request.GET.get('fecha_ingreso'),  
    'fecha_egreso': request.GET.get('fecha_salida'),   
    'cantidad_personas': request.GET.get('cantidad_personas'),
    'cantidad_habitaciones': request.GET.get('cantidad_habitaciones'),
    }

    tipo = request.GET.get('tipo')
    id_origen = request.GET.get('id')

    hoteles = []
    error = None

    if tipo and id_origen:
            hoteles = buscarHotel(id_origen, tipo)

    if not hoteles:
        error = "No se encontraron hoteles para esa zona"


    return render(request, 'lista_hoteles.html', {
        'hoteles': hoteles,
        'error': error
    })

def detalle_hotel(request, id):
    # 1. Buscar hoteles por localidad
    hoteles = buscarHotel(id, 'localidad')

    # 2. Tomar el primer hotel (siempre será uno solo en detalle)
    hotel = None
    if hoteles:
        hotel = hoteles[0]

    request.session['id_hotel'] = id
    #request.session['id_hotel'] = hotel[0]

    # 3. Obtener las categorías de ese hotel
    categorias = mostrarHabitacionesHotel(hotel['id']) if hotel else []

    # 4. Para cada categoría, agregar sus servicios
    for cat in categorias:
        id_cat = cat.get('id')  # asegurate que mostrarHabitacionesHotel devuelva el campo "id"
        cat['servicios'] = mostrarServiciosCategorias(id_cat)

    # 5. Obtener los servicios de ese hotel
    servicios = mostrarServiciosHotel(hotel['id']) if hotel else []

    for cat in categorias:
        cat_id = cat.get('id')
    cat['servicios'] = mostrarServiciosCategorias(cat_id)


    return render(request, 'detalle_hotel.html', {
        'hotel': hotel,
        'categorias': categorias,
        'servicios' : servicios
    })

def seleccionar_categoria(request):
    if request.method == 'POST':
        id_categoria = request.POST.get('id_categoria')
        if id_categoria:
            request.session['id_categoria_seleccionada'] = id_categoria
            return redirect('hotel:detalle_reserva')  # va al finalizar reserva
    return redirect('hotel:buscar_alojamientos')  # redirige si falla

def calcular_total_reserva(request,precio_unitario,cantidad_noches):

    #Obtenemos los datos de la sesion
    datos = request.session.get('busqueda')

    #Obtenemos y convertimos la cantidad de habitaciones
    cantidad_hab = int(datos.get('cantidad_habitaciones') or 1)

    #Obtenemos el precio final de la reserva
    subtotal = precio_unitario * cantidad_hab * cantidad_noches
    #Calculamos los impuestos
    impuestos_tasas = subtotal * 0.21
    #Calculamos los cargos (comisiones del sitio o plataforma,costos por gestión de reserva, seguros, etc.)
    cargos = subtotal * 0.05
    precio_reserva = subtotal + impuestos_tasas + cargos
    #Formateamos para que se muestre de forma correcta
    precio_formateado = f"{subtotal:,.0f}".replace(",", ".")
    cargos_formateado = f"{cargos:,.0f}".replace(",", ".")
    impuestos_formateado = f"{impuestos_tasas:,.0f}".replace(",", ".")
    precio_final = f"{precio_reserva:,.0f}".replace(",", ".")

    return[precio_formateado,cargos_formateado,impuestos_formateado,precio_final]

def calcular_habitaciones_por_persona(request):
    #Obtenemos los datos de la sesion
    datos = request.session.get('busqueda')

    # Recuperamos la cantidad de personas de la sesión 
    personas_str = datos.get('cantidad_personas')
    try:
        personas = int(personas_str) if personas_str else 1
    except ValueError:
        personas = 1  # valor por defecto si alguien rompe algo

    #Obtenemos los datos de la categoria seleccionada
    id_categoria = request.session.get('id_categoria_seleccionada')
    categoria = buscarCategoriaPorId(id_categoria)
    capacidad_categoria = categoria[0]['capacidad_categoria'] 

    # Cálculo obligatorio para que nadie duerma en el pasillo
    habitaciones_requeridas = math.ceil(personas / capacidad_categoria)

    return habitaciones_requeridas

def regis_reservas_hoteles(request,precio_final):

    datos = request.session.get('busqueda')
    #Obtenemos el precio final de la reserva
    #precio_final

    #Obtenemos la fecha de la reserva

    #Obtenemos las fechas
    fecha_ingreso = datos.get('fecha_ingreso')  # '2025-06-23'
    fecha_egreso = datos.get('fecha_egreso')    # '2025-06-29'

    #Guardamos el id del estado de la reserva
    estado_reserva_id = 1 # Confirmada

    #Obtenemos el id del viajero
    id_viajero = request.session.get('id_viajero')

def guardar_datos_viajero(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_viajero')
        apellido = request.POST.get('apellido_viajero')
        identificacion = request.POST.get('identificacion_viajero')
        email = request.POST.get('email_viajero')
        telefono = request.POST.get('telefono_viajero')
        fecha_nacimiento = request.POST.get('fecha_nacimiento_viajero')
        clave = request.POST.get('clave_viajero')

        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO Viajeros 
                    (identificacion_viajero, nombre_viajero, apellido_viajero, telefono_viajero, 
                     email_viajero, fecha_nacimiento_viajero, clave_viajero)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, [
                    identificacion, nombre, apellido, telefono,
                    email, fecha_nacimiento, clave
                ])
        except Exception as e:
            print("Error al guardar el viajero:", e)
            return render(request, 'index_reserva.html', {
                'error': 'No se pudo guardar el viajero. Revisá los datos.'
            })

        # Redireccionar o continuar con la reserva
        return redirect('hotel:finalizar_reserva')  # Cambiá esto si querés otra ruta

    return redirect('hotel:detalle_reserva')


def guardar_datos_viajero(request):
    if request.method == 'POST':
        identificacion = request.POST.get('identificacion_viajero')
        nombre = request.POST.get('nombre_viajero')
        apellido = request.POST.get('apellido_viajero')
        email = request.POST.get('email_viajero')
        codigo_pais = request.POST.get('codigo_pais')
        telefono = request.POST.get('telefono_viajero')
        fecha_nacimiento = request.POST.get('fecha_nacimiento_viajero')
        clave = request.POST.get('clave_viajero')

        telefono_viajero = codigo_pais + telefono

        print("",nombre,apellido,identificacion,email,telefono_viajero,fecha_nacimiento,clave)

        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("EXEC insertarViajero %s, %s, %s, %s, %s, %s, %s", [
                    identificacion, nombre, apellido, telefono,
                    email, fecha_nacimiento, clave
                ])
        except Exception as e:
            print("Error al guardar el viajero:", e)
            return render(request, 'index_reserva.html', {
                'error': 'No se pudo guardar el viajero. Revisá los datos.'
            })
        """

        # Redireccionar o continuar con la reserva
        return redirect('hotel:buscar_alojamientos')  # Reemplaza por el nombre correcto si tenés otra vista

    return redirect('hotel:detalle_reserva')


def detalle_reserva(request):
    locale.setlocale(locale.LC_TIME, 'Spanish_Argentina') # Para formato en español 
    
    #Obtenemos los datos de la sesion
    datos = request.session.get('busqueda')
    #Obtenemos el id del hotel
    id_hotel = request.session.get('id_hotel')
    hotel = buscarHotelPorId(id_hotel)
    #Obtenemos la categoria de la habitación seleccionada
    id_categoria = request.session.get('id_categoria_seleccionada')
    categoria = buscarCategoriaPorId(id_categoria)

    
    #Obtenemos las fechas
    fecha_ingreso_str = datos.get('fecha_ingreso')  # '2025-06-23'
    fecha_egreso_str = datos.get('fecha_egreso')    # '2025-06-29'

    try:
        fecha_ingreso = datetime.strptime(fecha_ingreso_str, '%Y-%m-%d')
        fecha_egreso = datetime.strptime(fecha_egreso_str, '%Y-%m-%d')
    except Exception as e:
        print("Error al convertir fechas:", e)
        fecha_ingreso = fecha_egreso = None

    # Validamos fechas antes de restar
    if fecha_ingreso and fecha_egreso and fecha_egreso > fecha_ingreso:
        cantidad_noches = (fecha_egreso - fecha_ingreso).days
    else:
        cantidad_noches = 0
    #Transformamos a un formato mas agradable
    fecha_ingreso_fmt = fecha_ingreso.strftime('%a. %d %b. %Y').capitalize()
    fecha_egreso_fmt = fecha_egreso.strftime('%a. %d %b. %Y').capitalize()

    #Obtenemos la cantidad de estrellas del hotel
    estrellas = range(hotel[0]['cantidad_estrellas_hotel'])

    #Obtenemos el precio de cada categoria
    precio_unitario = float(categoria[0]['precio_categoria'])

    #obtenemos y convertimos los montos de la reserva
    precio_formateado=calcular_total_reserva(request,precio_unitario,cantidad_noches)[0]
    cargos_formateado=calcular_total_reserva(request,precio_unitario,cantidad_noches)[1]
    impuestos_formateado=calcular_total_reserva(request,precio_unitario,cantidad_noches)[2]
    precio_final=calcular_total_reserva(request,precio_unitario,cantidad_noches)[3]

    habitaciones_necesarias=range(calcular_habitaciones_por_persona(request))

    cantidad = calcular_habitaciones_por_persona(request)
    habitaciones_necesarias = range(cantidad)

    return render(request, 'index_reserva.html', {
        'datos': datos,
        'hotel': hotel[0],
        'categoria':categoria[0],
        'estrellas': estrellas,
        'precio_reserva':precio_formateado,
        'precio_final':precio_final,
        'impuestos':impuestos_formateado,
        'cargos':cargos_formateado,
        'fecha_ingreso_fmt': fecha_ingreso_fmt,
        'fecha_egreso_fmt': fecha_egreso_fmt,
        'cantidad_noches': cantidad_noches,
        'habitaciones_necesarias':habitaciones_necesarias
    })



