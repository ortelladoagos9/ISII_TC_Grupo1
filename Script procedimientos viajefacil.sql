--Procedimiento para obtener la lista de hoteles que se muestra en la pag ppal de Alojamientos
CREATE PROCEDURE obtenerHoteles
AS
BEGIN
  SET NOCOUNT ON;
SELECT h.id,
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
exec mostrarHabitacionesHotel 1
select * from Hoteles_Categorias where Hoteles_Categorias.id = 2
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

CREATE PROCEDURE insertarViajero
    @identificacion NVARCHAR(20),
    @nombre NVARCHAR(100),
    @apellido NVARCHAR(100),
    @telefono NVARCHAR(20),
    @email NVARCHAR(254),
    @fecha_nacimiento DATE,
    @clave NVARCHAR(128),
	@direccion_id INT
AS
BEGIN
    SET NOCOUNT ON;
    INSERT INTO Viajeros (
        identificacion_viajero,
        nombre_viajero,
        apellido_viajero,
        telefono_viajero,
        email_viajero,
        fecha_nacimiento_viajero,
        clave_viajero,
		direccion_id
    )
    VALUES (
        @identificacion,@nombre,@apellido,@telefono,@email,@fecha_nacimiento,@clave,@direccion_id);
END;

--Procedimiento para guardar la direccion
CREATE PROCEDURE insertarDireccionCompleta
    @nombre_pais NVARCHAR(100),
    @nombre_provincia NVARCHAR(100),
    @nombre_localidad NVARCHAR(100),
    @calle NVARCHAR(100),
    @numero NVARCHAR(10),
    @codigo_postal NVARCHAR(20),
    @id_direccion BIGINT OUTPUT
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @id_pais BIGINT, @id_provincia BIGINT, @id_localidad BIGINT;

    -- 1. Buscar o insertar país
    SELECT @id_pais = id FROM Paises 
    WHERE nombre_pais COLLATE Latin1_General_CI_AI = @nombre_pais COLLATE Latin1_General_CI_AI;
    IF @id_pais IS NULL
    BEGIN
        INSERT INTO Paises (nombre_pais) VALUES (@nombre_pais);
        SET @id_pais = SCOPE_IDENTITY();
    END

    -- 2. Buscar o insertar provincia
    SELECT @id_provincia = id FROM Provincias 
    WHERE nombre_provincia COLLATE Latin1_General_CI_AI = @nombre_provincia COLLATE Latin1_General_CI_AI
      AND pais_id = @id_pais;
    IF @id_provincia IS NULL
    BEGIN
        INSERT INTO Provincias (nombre_provincia, pais_id) 
        VALUES (@nombre_provincia, @id_pais);
        SET @id_provincia = SCOPE_IDENTITY();
    END

    -- 3. Buscar o insertar localidad
    SELECT @id_localidad = id FROM Localidades 
    WHERE nombre_localidad COLLATE Latin1_General_CI_AI = @nombre_localidad COLLATE Latin1_General_CI_AI
      AND provincia_id = @id_provincia;
    IF @id_localidad IS NULL
    BEGIN
        INSERT INTO Localidades (nombre_localidad, provincia_id)
        VALUES (@nombre_localidad, @id_provincia);
        SET @id_localidad = SCOPE_IDENTITY();
    END

    -- 4. Buscar o insertar dirección
    SELECT @id_direccion = id FROM Direcciones 
    WHERE calle_direccion COLLATE Latin1_General_CI_AI = @calle COLLATE Latin1_General_CI_AI
      AND numero_direccion = @numero
      AND cod_postal = @codigo_postal
      AND localidad_id = @id_localidad;
    IF @id_direccion IS NULL
    BEGIN
        INSERT INTO Direcciones (calle_direccion, numero_direccion, cod_postal, localidad_id)
        VALUES (@calle, @numero, @codigo_postal, @id_localidad);
        SET @id_direccion = SCOPE_IDENTITY();
    END
END;
