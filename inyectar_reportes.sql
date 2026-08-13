-- Inserción múltiple de los datos extraídos de los PDFs manuscritos
INSERT INTO reportes_comunitarios (nombre, documento, telefono, direccion, barrio, personas_afectadas, observaciones) 
VALUES
('Emperatriz Mayorga', '31472973', '3175122852 - 3105105027', 'Cra 2 # 15-20', 'FRAY PEÑA', 5, '2 adultos mayores, 2 jovenes, 1 niño.'),
('Ana Lucia Rengifo', '38992373', '3175258614', 'Cra 10 # 8-26', 'URIBE', 2, '2 adultos mayores.'),
('Dilan Ordoñez', 'No registrado', '3215661749', 'Cra 3H 15B-48', 'FRAY PEÑA', 4, 'Daño estructural en el techo. 2 adultos mayores, 1 adulto con discapacidad, 1 menor de edad.'),
('Alba Noguera Martinez', '66857031', '3116322686 - 3007301463', 'Calle 9 # 17-53', 'SIN ESPECIFICAR', 2, 'Sin observaciones.'),
('Arlex Ortega', '16837186', '3102470015 - 3206403991', 'Carrera 5 # 5-36', 'BELLAVISTA', 3, 'Sin observaciones.'),
('Consuelo Lugo Arias', 'No registrado', '3219808707 - 3028683247', 'Cra 9 Norte # 5N-44', 'BELLAVISTA', 6, 'Vivienda de 3 pisos. Casa con afectacion en estructura y paredes con inclinación. 1 adulto mayor, 1 bebe.'),
('Leidy Alejandra Cardozo', 'No registrado', '3128212518', 'Calle 5 Oeste # 4C-33', 'NUEVO HORIZONTE', 6, '2 niñas (1 con discapacidad). Afectaciones en piso 1 y 2.'),
('Laura Albear Ruiz (Admin)', 'NIT 901-756-456-8', '318-320-22-26', 'Conj. Res. Golondrina de la Colina', 'SIN ESPECIFICAR', 0, 'Solicitud de verificar 4 torres (3 de 10 pisos, 1 de 8 pisos). 304 apartamentos. Ya asistió Bomberos.'),
('Edwin Ramos Gallego', 'No registrado', '3185571880 - 3005960939', 'Cra 3 # 13A-81', 'TRINIDAD', 3, '2 adultos, 1 menor. Vivienda con agrietamiento y estructura muy afectada.');
