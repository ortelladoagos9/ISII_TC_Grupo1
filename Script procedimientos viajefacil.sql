--Procedimiento para obtener la lista de hoteles que se muestra en la pag ppal de Alojamientos
CREATE PROCEDURE obtenerHoteles
AS
BEGIN
  SET NOCOUNT ON;
SELECT h.nombre_hotel, h.cantidad_estrellas_hotel,
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
            h.id,
            h.nombre_hotel, 
            h.descripcion_hotel,
            CONCAT(p.nombre_provincia, ', ', l.nombre_localidad, '. ',
                   d.calle_direccion, ' ', d.numero_direccion) AS Direccion,
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
            h.id,
            h.nombre_hotel, 
            h.descripcion_hotel,
            CONCAT(l.nombre_localidad, ', ', p.nombre_provincia, '. ',
                   d.calle_direccion, ' ', d.numero_direccion) AS Direccion,
            h.cantidad_estrellas_hotel
        FROM Hoteles h
        INNER JOIN Direcciones d ON h.ID_direccion_id = d.ID
        INNER JOIN Localidades l ON d.localidad_id = l.id
        INNER JOIN Provincias p ON l.provincia_id = p.id
        WHERE l.id = @id_direccion;
    END
END
--Procedimiento para el autocompletado en la busqueda de hoteles
CREATE PROCEDURE busquedaDestinos
    @termino NVARCHAR(100)
AS
BEGIN
    -- Resultados por localidad
    SELECT 
        CONCAT(l.nombre_localidad, ', ', p.nombre_provincia) AS destino,
        'localidad' AS tipo,
        l.id AS id
    FROM Localidades l
    INNER JOIN Provincias p ON l.id = p.id
    WHERE l.nombre_localidad COLLATE Latin1_General_CI_AI LIKE '%' + @termino + '%'
    UNION
    -- Resultados por provincia
    SELECT 
        p.nombre_provincia AS destino,
        'provincia' AS tipo,
        p.id AS id
    FROM Provincias p
    WHERE p.nombre_provincia COLLATE Latin1_General_CI_AI LIKE '%' + @termino + '%'
    ORDER BY destino
END

--Procedimiento para mostrar todas las categorias de un hotel
CREATE PROCEDURE mostrarHabitacionesHotel
    @id_hotel INT
AS
BEGIN
  SET NOCOUNT ON;
	SELECT
	hc.id as id,
	h.nombre_hotel, c.nombre_categoria, c.descripcion_categoria, c.capacidad_categoria,
	FORMAT(c.precio_categoria, 'N2', 'es-AR') as precio_categoria
	FROM Hoteles_Categorias hc
	JOIN Hoteles h ON hc.hotel_id = h.id
	JOIN Categorias c ON hc.categoria_id = c.id
	where h.id=@id_hotel
	ORDER BY h.nombre_hotel, c.nombre_categoria
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
