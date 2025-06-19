from django.db import connection


def obtenerHoteles():
    with connection.cursor() as cursor:
        cursor.execute("EXEC obtenerHoteles")
        columnas = [col[0] for col in cursor.description]
        return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
    

def buscarHotel(id_direccion, tipo):
    with connection.cursor() as cursor:
        cursor.execute("EXEC buscarHotel %s, %s", [id_direccion, tipo])
        filas = cursor.fetchall()
        
        if not filas:
            return []  # No hay datos

        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in filas]
        return resultados
    
def buscarHotelPorId(id_hotel):
    with connection.cursor() as cursor:
        cursor.execute("EXEC buscarHotelPorId %s", [id_hotel])
        filas = cursor.fetchall()
        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in filas]
        return resultados

def mostrarHabitacionesHotel(id_hotel):
    with connection.cursor() as cursor:
        cursor.execute("EXEC mostrarHabitacionesHotel %s", [id_hotel])
        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        return resultados


def mostrarServiciosHotel(id_hotel):
    with connection.cursor() as cursor:
        cursor.execute("EXEC mostrarServiciosHotel %s", [id_hotel])
        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        return resultados
    
def mostrarServiciosCategorias(id_categoria):
    with connection.cursor() as cursor:
        cursor.execute("EXEC mostrarServiciosCategorias %s", [id_categoria])
        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        return resultados
    
def buscarCategoriaPorId(id_categoria):
    with connection.cursor() as cursor:
        cursor.execute("EXEC buscarCategoriaPorId %s", [id_categoria])
        columnas = [col[0] for col in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]
        return resultados

from django.db import connection

def insertarViajero(data):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                EXEC insertarViajero 
                    @identificacion=%s,
                    @nombre=%s,
                    @apellido=%s,
                    @telefono=%s,
                    @email=%s,
                    @fecha_nacimiento=%s,
                    @clave=%s
            """, [
                data['identificacion_viajero'],
                data['nombre_viajero'],
                data['apellido_viajero'],
                data['telefono_viajero'],
                data['email_viajero'],
                data['fecha_nacimiento_viajero'],
                data['clave_viajero']
            ])
        return True
    except Exception as e:
        print("Error al insertar viajero:", e)
        return False
