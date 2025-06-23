--Procedimiento para obtener la lista de hoteles que se muestra en la pag ppal de Alojamientos
CREATE PROCEDURE obtenerHoteles
AS
BEGIN
  SET NOCOUNT ON;
SELECT h.id,h.imagen_hotel,
h.nombre_hotel, h.cantidad_estrellas_hotel,
CONCAT(p.nombre_provincia, ', ', l.nombre_localidad, '. ',
d.calle_direccion, ' ', d.numero_direccion) as direccion
FROM Hoteles h
INNER JOIN Direcciones d ON h.ID_direccion_id = d.ID
INNER JOIN Localidades l ON d.localidad_id = l.id
INNER JOIN Provincias p ON l.provincia_id = p.id
END;

--Procedimiento para realizar la busqueda de hotel por provincia o localidad según usuario
CREATE PROCEDURE buscarHotel
    @id_direccion INT,
    @tipo NVARCHAR(20)  -- puede ser 'provincia' o 'localidad'
AS
BEGIN
    SET NOCOUNT ON;
    SET @tipo = LTRIM(RTRIM(LOWER(@tipo)));
    IF @tipo = 'provincia'
    BEGIN
        SELECT 
			h.imagen_hotel,
            h.id,h.nombre_hotel, h.descripcion_hotel,
            CONCAT(p.nombre_provincia, ', ', l.nombre_localidad, '. ',d.calle_direccion, ' ', d.numero_direccion) AS Direccion,
            h.cantidad_estrellas_hotel
        FROM Hoteles h
        INNER JOIN Direcciones d ON h.ID_direccion_id = d.ID
        INNER JOIN Localidades l ON d.localidad_id = l.id
        INNER JOIN Provincias p ON l.provincia_id = p.id
        WHERE p.id = @id_direccion;
    END
    ELSE IF @tipo = 'localidad'
    BEGIN
        SELECT 
		h.imagen_hotel,
            h.id,h.nombre_hotel, h.descripcion_hotel,
            CONCAT(l.nombre_localidad, ', ', p.nombre_provincia, '. ',
                   d.calle_direccion, ' ', d.numero_direccion) AS Direccion,h.cantidad_estrellas_hotel
        FROM Hoteles h
        INNER JOIN Direcciones d ON h.ID_direccion_id = d.ID
        INNER JOIN Localidades l ON d.localidad_id = l.id
        INNER JOIN Provincias p ON l.provincia_id = p.id
        WHERE l.id = @id_direccion;
    END
END

-- Procedimiento para el autocompletado en la búsqueda de hoteles
CREATE PROCEDURE busquedaDestinos
    @termino NVARCHAR(100)
AS
BEGIN
    SET NOCOUNT ON;
    -- Solo mostrar resultados por localidad
    SELECT 
        CONCAT(l.nombre_localidad, ', ', p.nombre_provincia, ', ', pa.nombre_pais) AS destino,
        'localidad' AS tipo,
        l.id AS id
    FROM Localidades l
    INNER JOIN Provincias p ON l.provincia_id = p.id
    INNER JOIN Paises pa ON p.pais_id = pa.id
    WHERE l.nombre_localidad COLLATE Latin1_General_CI_AI LIKE '%' + @termino + '%'
    ORDER BY destino;
END
--Procedimiento para mostrar todas las categorias de un hotel
CREATE PROCEDURE buscarHabitacionesDisponibles
    @id_hotel INT,
    @fecha_ingreso DATE,
	@fecha_egreso DATE
AS
BEGIN
    SET NOCOUNT ON;
    SELECT 
        hc.id AS id_relacion,h.nombre_hotel,c.id AS id_categoria,
        c.nombre_categoria,c.descripcion_categoria,c.capacidad_categoria,dc.cantidad_disponible,c.imagen_categoria,
        FORMAT(c.precio_categoria, 'N2', 'es-AR') AS precio_categoria
    FROM Hoteles_Categorias hc
    JOIN Hoteles h ON hc.hotel_id = h.id
    JOIN Categorias c ON hc.categoria_id = c.id
    JOIN Disponibilidad_Categorias dc ON dc.categoria_id = c.id
    WHERE 
        h.id = @id_hotel
		AND dc.fecha <= @fecha_ingreso
    ORDER BY c.capacidad_categoria DESC;
END;
--Procedimiento para obtener los servicios del hotel
CREATE PROCEDURE mostrarServiciosHotel
    @id_hotel INT
AS
BEGIN
  SET NOCOUNT ON;
	SELECT
	sh.nombre_servicio
	FROM Hoteles h
	INNER JOIN Hoteles_Servicios s on s.hotel_id=h.id
	INNER JOIN Servicios_Hoteles sh on sh.id = s.servicio_hotel_id
	WHERE h.id = @id_hotel
	ORDER BY h.nombre_hotel;
END;
--Procedimiento para obtener los servicios de la habitacion
CREATE PROCEDURE mostrarServiciosCategorias
 @id_categoria INT
AS
BEGIN
  SET NOCOUNT ON;
	SELECT
	sch.nombre_servicio
	FROM Categorias_Servicios cs
	INNER JOIN Categorias c on c.id=cs.categoria_id
	INNER JOIN Servicios_Categorias_Habitaciones sch on sch.id = cs.servicio_hotel_id
	WHERE cs.categoria_id = @id_categoria
	ORDER BY sch.nombre_servicio;
END;

--Procedimiento para buscar hotel por id para mostrar en el index reserva
CREATE PROCEDURE buscarHotelPorId
@id_hotel INT
AS
BEGIN
	SET NOCOUNT ON;
	SELECT h.nombre_hotel,h.cantidad_estrellas_hotel,
	CONCAT(p.nombre_provincia, ', ', l.nombre_localidad, '. ',
					   d.calle_direccion, ' ', d.numero_direccion) AS Direccion
	FROM Hoteles H
	INNER JOIN Direcciones d ON h.ID_direccion_id = d.ID
	INNER JOIN Localidades l ON d.localidad_id = l.id
	INNER JOIN Provincias p ON l.provincia_id = p.id
	WHERE h.id = @id_hotel
END;
--Procedimiento para buscar categoria por id para mostrar en la reserva
CREATE PROCEDURE buscarCategoriaPorId
@id_categoria INT
AS
BEGIN
	SET NOCOUNT ON;
	SELECT c.nombre_categoria, c.descripcion_categoria, c.precio_categoria,c.capacidad_categoria
	FROM hoteles_categorias hc
	INNER JOIN Categorias c on hc.categoria_id=c.id
	WHERE hc.id = @id_categoria
END;
--Procedimiento para insertar viajero
CREATE PROCEDURE ingresarDatos
    @identificacion NVARCHAR(20),
    @nombre NVARCHAR(100),
    @apellido NVARCHAR(100),
    @telefono NVARCHAR(20),
    @email NVARCHAR(254),
    @fecha_nacimiento DATE,
    @clave NVARCHAR(128),
    @direccion_id BIGINT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @nuevo_id BIGINT;
    INSERT INTO Viajeros (
        identificacion_viajero,nombre_viajero,apellido_viajero,telefono_viajero,email_viajero,
        fecha_nacimiento_viajero,clave_viajero,direccion_id)
    VALUES (
        @identificacion,@nombre,@apellido,@telefono,@email,@fecha_nacimiento,@clave,@direccion_id
    );
    -- Obtener el ID generado
    SET @nuevo_id = SCOPE_IDENTITY();
    -- Retornar el ID del viajero insertado
    SELECT @nuevo_id AS id_viajero;
END

-- Este procedimiento recibe los campos y devuelve el ID de la dirección si ya existe,
-- y si no existe, la crea y luego lo devuelve.
CREATE PROCEDURE verificarOCrearDireccion
    @pais NVARCHAR(100),
    @provincia NVARCHAR(100),
    @localidad NVARCHAR(100),
    @calle NVARCHAR(100),
    @numero NVARCHAR(20),
    @codigo_postal NVARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @pais_id BIGINT, @provincia_id BIGINT, @localidad_id BIGINT, @direccion_id BIGINT;
    -- Buscar o insertar país
    SELECT @pais_id = id FROM Paises WHERE LOWER(nombre_pais) = LOWER(@pais);
    IF @pais_id IS NULL
    BEGIN
        INSERT INTO Paises(nombre_pais) VALUES (@pais);
        SET @pais_id = SCOPE_IDENTITY();
    END
    -- Buscar o insertar provincia
    SELECT @provincia_id = id FROM Provincias WHERE LOWER(nombre_provincia) = LOWER(@provincia) AND pais_id = @pais_id;
    IF @provincia_id IS NULL
    BEGIN
        INSERT INTO Provincias(nombre_provincia, pais_id) VALUES (@provincia, @pais_id);
        SET @provincia_id = SCOPE_IDENTITY();
    END
    -- Buscar o insertar localidad
    SELECT @localidad_id = id FROM Localidades WHERE LOWER(nombre_localidad) = LOWER(@localidad) AND provincia_id = @provincia_id;
    IF @localidad_id IS NULL
    BEGIN
        INSERT INTO Localidades(nombre_localidad, provincia_id) VALUES (@localidad, @provincia_id);
        SET @localidad_id = SCOPE_IDENTITY();
    END
    -- Buscar o insertar dirección
    SELECT @direccion_id = id FROM Direcciones
    WHERE LOWER(calle_direccion) = LOWER(@calle)
      AND numero_direccion = @numero
      AND cod_postal = @codigo_postal
      AND localidad_id = @localidad_id;
    IF @direccion_id IS NULL
    BEGIN
        INSERT INTO Direcciones(calle_direccion, numero_direccion, cod_postal, localidad_id)
        VALUES (@calle, @numero, @codigo_postal, @localidad_id);
        SET @direccion_id = SCOPE_IDENTITY();
    END
    SELECT @direccion_id AS direccion_id;
END

--Procedimiento para insertar la cabecera de la reserva del hotel
CREATE PROCEDURE insertarCabeceraReservaHotel
    @monto_total NUMERIC(10,2),
    @fecha_reserva DATE,
    @fecha_ingreso DATE,
    @fecha_egreso DATE,
    @estado_reserva_id BIGINT,
    @viajero_id BIGINT
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @nueva_reserva_id BIGINT;
    INSERT INTO Reservas_Hoteles (
	monto_total_hotel,fecha_reserva,fecha_ingreso,fecha_egreso,estado_reserva_id,viajero_id)

    VALUES (@monto_total,@fecha_reserva,@fecha_ingreso,@fecha_egreso,@estado_reserva_id,@viajero_id);
    SET @nueva_reserva_id = SCOPE_IDENTITY();
	--Devolvemos el id
    SELECT @nueva_reserva_id AS id_reserva_hotel;
END

--Procedimiento para insertar el/los detalles de las categorias de la reserva
CREATE PROCEDURE insertarDetalleReservaHotel
    @cantidad_habitaciones INT,
    @precio_unitario NUMERIC(10,2),
    @sub_total NUMERIC(12,2),
    @categoria_id BIGINT,
    @reserva_hotel_id BIGINT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Reservas_Hoteles_Detalles (
        cantidad_habitaciones,precio_unitario,sub_total,categoria_id,reserva_hotel_id)
    VALUES (@cantidad_habitaciones,@precio_unitario,@sub_total,@categoria_id,@reserva_hotel_id);
END

--Procedimiento para generar la factura pasandole el id de la reserva
CREATE PROCEDURE generarFactura
    @id_reserva INT
AS
BEGIN
    SET NOCOUNT ON;
    --------------------------------------
    -- 1. DATOS DEL VIAJERO
    --------------------------------------
    SELECT 
        v.identificacion_viajero,
        CONCAT(v.nombre_viajero,' ',v.apellido_viajero) AS nombre_completo,
        v.email_viajero,
        v.telefono_viajero,
        CONCAT(d.calle_direccion, ', ', d.numero_direccion, ', ', l.nombre_localidad, ', ', 
               p.nombre_provincia, ', ', pa.nombre_pais) AS direccion_viajero
    FROM Reservas_Hoteles rh
    INNER JOIN Viajeros v ON v.id = rh.viajero_id
    INNER JOIN Direcciones d ON d.id = v.direccion_id
    INNER JOIN Localidades l ON l.id = d.localidad_id
    INNER JOIN Provincias p ON p.id = l.provincia_id
    INNER JOIN Paises pa ON pa.id = p.pais_id
    WHERE rh.id = @id_reserva;
    --------------------------------------
    -- 2. DATOS DE LA CABECERA
    --------------------------------------
    SELECT 
        rh.id AS nro_reserva,
        rh.fecha_reserva,
        rh.fecha_ingreso AS checkin,
        rh.fecha_egreso AS checkout,
        DATEDIFF(DAY, rh.fecha_ingreso, rh.fecha_egreso) AS noches,
        er.descripcion_estado_reserva AS estado,
        rh.monto_total_hotel AS monto_total_reserva
    FROM Reservas_Hoteles rh
    INNER JOIN Estados_Reservas er ON er.id = rh.estado_reserva_id
    WHERE rh.id = @id_reserva;

    --------------------------------------
    -- 3. DATOS DEL HOTEL
    --------------------------------------
	SELECT h.nombre_hotel,
	CONCAT(d.calle_direccion, ' ', d.numero_direccion, '. ', l.nombre_localidad, ', ', 
               p.nombre_provincia, '. ', pa.nombre_pais) AS direccion_hotel
	FROM Reservas_Hoteles rh
	JOIN Hoteles h ON h.id = rh.hotel_id
	INNER JOIN Direcciones d ON d.id = h.ID_direccion_id
    INNER JOIN Localidades l ON l.id = d.localidad_id
    INNER JOIN Provincias p ON p.id = l.provincia_id
    INNER JOIN Paises pa ON pa.id = p.pais_id
	WHERE rh.id = @id_reserva
    --------------------------------------
    -- 4. DETALLES DE LA RESERVA (CATEGORÍAS)
    --------------------------------------
    SELECT 
        CONCAT(c.nombre_categoria, ' (', c.descripcion_categoria, ')') AS categoria,
        rhd.cantidad_habitaciones,
        rhd.precio_unitario,
        rhd.sub_total
    FROM Reservas_Hoteles_Detalles rhd
    INNER JOIN Categorias c ON c.id = rhd.categoria_id
    WHERE rhd.reserva_hotel_id = @id_reserva;
END;

--Procedimiento para cancelar la reserva
CREATE PROCEDURE cancelarReserva
	@id_reserva INT
AS
	BEGIN
	UPDATE rh
	SET rh.estado_reserva_id=2
	FROM Reservas_Hoteles rh
	WHERE id=@id_reserva
END;

--Procedimiento para habilitar la reserva
CREATE PROCEDURE habilitarReserva
	@id_reserva INT
AS
	BEGIN
	UPDATE rh
	SET rh.estado_reserva_id=1
	FROM Reservas_Hoteles rh
	WHERE id=@id_reserva
END;
--Procedimiento para obtener las reservas del viajero
CREATE PROCEDURE obtenerReservas
	@id_viajero INT
AS
BEGIN
	SET NOCOUNT ON;
	select 
	rs.id,rs.fecha_ingreso,fecha_egreso,
	rs.monto_total_hotel,rs.fecha_reserva,er.descripcion_estado_reserva,h.nombre_hotel
	from Reservas_Hoteles rs
	INNER JOIN Estados_Reservas er on er.id=rs.estado_reserva_id
	INNER JOIN Hoteles h on h.id=rs.hotel_id
	where rs.viajero_id=@id_viajero
END;



