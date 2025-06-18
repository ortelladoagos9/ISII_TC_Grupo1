--Script para crear la base
CREATE DATABASE viajefacil
USE viajefacil
--Script para insertar datos en la base
--Agregamos el país
SET IDENTITY_INSERT Paises ON;
INSERT INTO Paises (id, nombre_pais)
VALUES (1, 'Argentina');
SET IDENTITY_INSERT Paises OFF;
--Agregamos las provincias
SET IDENTITY_INSERT Provincias ON;
INSERT INTO Provincias (id, nombre_provincia, pais_id)
VALUES 
(1, 'Buenos Aires', 1),
(2, 'Córdoba', 1),
(3, 'Mendoza', 1),
(4, 'Santa Fe', 1),
(5, 'Río Negro', 1);
SET IDENTITY_INSERT Provincias OFF;

--Agregamos las localidades
SET IDENTITY_INSERT Localidades ON;
INSERT INTO Localidades (id, nombre_localidad, provincia_id)
VALUES
(1, 'Mar del Plata', 1),
(2, 'La Plata', 1),
(3, 'Villa Carlos Paz', 2),
(4, 'Córdoba Capital', 2),
(5, 'Mendoza Capital', 3),
(6, 'San Rafael', 3),
(7, 'Rosario', 4),
(8, 'Santa Fe Capital', 4),
(9, 'Bariloche', 5),
(10, 'El Bolsón', 5);
SET IDENTITY_INSERT Localidades OFF;
--Agregamos las direcciones
SET IDENTITY_INSERT Direcciones ON;
INSERT INTO Direcciones (id, calle_direccion, numero_direccion, cod_postal, localidad_id)
VALUES
(1, 'Av. Colón', 1234, '7600', 1),
(2, 'Calle 12', 456, '1900', 2),
(3, 'Av. Libertad', 789, '5152', 3),
(4, 'Av. General Paz', 234, '5000', 4),
(5, 'Calle Belgrano', 890, '5500', 5),
(6, 'Ruta 143', 321, '5600', 6),
(7, 'Bv. Oroño', 654, '2000', 7),
(8, 'Calle Urquiza', 987, '3000', 8),
(9, 'Av. Bustillo', 111, '8400', 9),
(10, 'Ruta 40', 222, '8430', 10);
SET IDENTITY_INSERT Direcciones OFF;
--Agregamos los hoteles
SET IDENTITY_INSERT Hoteles ON;
INSERT INTO Hoteles (id, nombre_hotel, descripcion_hotel, cantidad_estrellas_hotel, imagen_hotel, ID_direccion_id)
VALUES 
(1, 'Hotel Mar Azul', 'Frente al mar, ideal para vacaciones familiares.', 4, NULL, 1),
(2, 'La Plata Suites', 'Moderno hotel en el centro de la ciudad.', 3, NULL, 2),
(3, 'Carlos Paz Inn', 'Vista al lago San Roque, excelente ubicación.', 4, NULL, 3),
(4, 'Córdoba Centro Hotel', 'Confort y cercanía al casco histórico.', 3, NULL, 4),
(5, 'Mendoza Andes Resort', 'Vistas a la cordillera y viñedos.', 5, NULL, 5),
(6, 'San Rafael EcoHotel', 'Hotel ecológico con actividades al aire libre.', 4, NULL, 6),
(7, 'Rosario Park Hotel', 'Ubicado frente al Parque Independencia.', 4, NULL, 7),
(8, 'Santa Fe Plaza', 'Cerca de centros culturales y del río.', 3, NULL, 8),
(9, 'Bariloche Snow', 'Hotel boutique con vista al Nahuel Huapi.', 5, NULL, 9),
(10, 'El Bolsón Lodge', 'Ideal para amantes del trekking y la naturaleza.', 4, NULL, 10);
SET IDENTITY_INSERT Hoteles OFF;
--Agregamos los servicios del hotel
SET IDENTITY_INSERT Servicios_Hoteles ON;
INSERT INTO Servicios_Hoteles (id, nombre_servicio)
VALUES 
(1, 'Wi-Fi gratis en zonas comunes'),
(2, 'TV en zonas comunes'),
(3, 'Terraza'),
(4, 'Desayuno'),
(5, 'Estacionamiento con costo adicional'),
(6, 'Ascensor'),
(7, 'Accesible para personas con movilidad reducida'),
(8, 'Computadora para huéspedes'),
(9, 'Caja fuerte en la recepción'),
(10, 'Servicio de guarda-equipaje ');
SET IDENTITY_INSERT Servicios_Hoteles OFF;
--Establecemos la relacion de los servicios con los hoteles
SET IDENTITY_INSERT Hoteles_Servicios ON;
INSERT INTO Hoteles_Servicios (id, hotel_id, servicio_hotel_id)
VALUES 
(1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), (5, 1, 5), (6, 1, 6), (7, 1, 7), (8, 1, 8), (9, 1, 9), (10, 1, 10),
(11, 2, 1), (12, 2, 2), (13, 2, 3), (14, 2, 4), (15, 2, 5), (16, 2, 6), (17, 2, 7), (18, 2, 8), (19, 2, 9), (20, 2, 10),
(21, 3, 1), (22, 3, 2), (23, 3, 3), (24, 3, 4), (25, 3, 5), (26, 3, 6), (27, 3, 7), (28, 3, 8), (29, 3, 9), (30, 3, 10),
(31, 4, 1), (32, 4, 2), (33, 4, 3), (34, 4, 4), (35, 4, 5), (36, 4, 6), (37, 4, 7), (38, 4, 8), (39, 4, 9), (40, 4, 10),
(41, 5, 1), (42, 5, 2), (43, 5, 3), (44, 5, 4), (45, 5, 5), (46, 5, 6), (47, 5, 7), (48, 5, 8), (49, 5, 9), (50, 5, 10),
(51, 6, 1), (52, 6, 2), (53, 6, 3), (54, 6, 4), (55, 6, 5), (56, 6, 6), (57, 6, 7), (58, 6, 8), (59, 6, 9), (60, 6, 10),
(61, 7, 1), (62, 7, 2), (63, 7, 3), (64, 7, 4), (65, 7, 5), (66, 7, 6), (67, 7, 7), (68, 7, 8), (69, 7, 9), (70, 7, 10),
(71, 8, 1), (72, 8, 2), (73, 8, 3), (74, 8, 4), (75, 8, 5), (76, 8, 6), (77, 8, 7), (78, 8, 8), (79, 8, 9), (80, 8, 10),
(81, 9, 1), (82, 9, 2), (83, 9, 3), (84, 9, 4), (85, 9, 5), (86, 9, 6), (87, 9, 7), (88, 9, 8), (89, 9, 9), (90, 9, 10),
(91, 10, 1), (92, 10, 2), (93, 10, 3), (94, 10, 4), (95, 10, 5), (96, 10, 6), (97, 10, 7), (98, 10, 8), (99, 10, 9), (100, 10, 10);
SET IDENTITY_INSERT Hoteles_Servicios OFF;
--Agregamos las categorias de las habitaciones
SET IDENTITY_INSERT Categorias ON;
INSERT INTO Categorias (id, nombre_categoria, descripcion_categoria, capacidad_categoria, precio_categoria)
VALUES 
(1, 'Estándar', 'Single', 1, 10000),
(2, 'Estándar', 'Doble', 2, 15000),
(3, 'Estándar', 'Triple', 3, 40000),
(4, 'Master', 'Single', 1, 15000),
(5, 'Master', 'Doble', 2, 35000),
(6, 'Master', 'Triple', 3, 50000),
(7, 'Suite', 'Single', 1, 20000),
(8, 'Suite', 'Doble', 2, 45000),
(9, 'Suite', 'Triple', 3, 60000);
SET IDENTITY_INSERT Categorias OFF;
--Agregamos los servicios de las habitaciones
SET IDENTITY_INSERT Servicios_Categorias_Habitaciones ON;
INSERT INTO Servicios_Categorias_Habitaciones (id, nombre_servicio)
VALUES 
(1, 'Armario'),
(2, 'Aire Acondicionado'),
(3, 'Ducha'),
(4, 'Smart TV'),
(5, 'Minibar')
SET IDENTITY_INSERT Servicios_Categorias_Habitaciones OFF;
-- Establecemos la relación entre categorías y servicios
SET IDENTITY_INSERT Categorias_Servicios ON;
INSERT INTO Categorias_Servicios (id, categoria_id, servicio_hotel_id)
VALUES 
--Servicios asignados a las habitaciones: Armario, Aire Acondicionado, Ducha
(1, 1, 1), (2, 1, 2), (3, 1, 3),
(4, 2, 1), (5, 2, 2), (6, 2, 3),
(7, 3, 1), (8, 3, 2), (9, 3, 3)
SET IDENTITY_INSERT Categorias_Servicios OFF;
--Asignamos las categorias a los hoteles
SET IDENTITY_INSERT Hoteles_Categorias ON;
INSERT INTO Hoteles_Categorias (id, hotel_id, categoria_id)
VALUES
-- Hotel 1: 2 Suites Dobles, 1 Estándar Triple
(1, 1, 8),
(2, 1, 3),
-- Hotel 2: 1 Master Doble, 2 Estándar Doble
(3, 2, 5),
(4, 2, 2),
-- Hotel 3: 1 Suite Triple, 1 Estándar Single, 1 Master Doble
(5, 3, 9),
(6, 3, 1),
(7, 3, 5),
-- Hotel 4: 3 Estándar Doble
(8, 4, 2),
-- Hotel 5: 1 Master Triple, 2 Suite Doble
(9, 5, 6),
(10, 5, 8),
-- Hotel 6: 1 Estándar Single, 1 Master Single
(11, 6, 1),
(12, 6, 4),
-- Hotel 7: 1 Suite Triple, 1 Estándar Doble, 1 Master Doble
(13, 7, 9),
(14, 7, 2),
(15, 7, 5),
-- Hotel 8: 2 Master Doble
(16, 8, 5),
-- Hotel 9: 2 Estándar Single, 1 Estándar Triple
(17, 9, 1),
(18, 9, 3),
-- Hotel 10: (variedad)
(19, 10, 1),
(20, 10, 2),
(21, 10, 3),
(22, 10, 4),
(23, 10, 5)
SET IDENTITY_INSERT Hoteles_Categorias OFF;

