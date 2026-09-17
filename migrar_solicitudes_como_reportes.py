import psycopg2
import uuid

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

SOLICITUDES = [
    ("Yury Ramos", "7718282642", "314 553 2343", "Cra 8 #2-14 B/ San Fernando", "2 adultos, 1 niña"),
    ("Disney Alicia Valdes Torres", "31468472", "3148889934", "Cra 4N #8-53 B/ Lleras", "2 adultas"),
    ("Diego Alexander Sanchez", "16927681", "312 855 4970", "Calle 9 #12-48 Belalcazar", "4 adultos, 2 niños. Ampliación de grietas"),
    ("Victoria Melo", "31170614", "310 388 7442", "Cra 15 B #22-04 B/ La Estancia Antigua", "Desocupada. Muros con grietas severas, columna quebrada"),
    ("Diana Correa Cardozo", "0", "318 267 4558", "Calle 5 Oeste #4C-43 Nuevo Horizonte", "1 persona con discapacidad. Columnas y grietas, vivienda desocupada"),
    ("Stefani Zuñiga", "1118305024", "305 313 9404", "Kra 13 A #15B-03 B/ Nueva Estancia La Esquina", "3 personas (2 adultos, 1 menor). Fisuras en fachada y techo"),
    ("Yofana Andrea Gonzalez Sanchez", "1118294853", "310 882 4157", "Cra 30 Calle 3A Casa 10 B/ Arroyohondo el Tablazo", "Fisuras y grietas"),
    ("Vinericth Lopez Ruiz", "0", "313 576 5386", "Calle 13IN #9N - Cacique Juanlo", "Techo en la parte posterior caído en su totalidad"),
    ("Yassica Torres", "0", "314 784 5188", "Cra 10 #6 AN-47 B/ Nita", "3 personas (2 niñas). Daños estructurales (Prioridad #3)"),
    ("Vicky Millarly", "0", "316 946 6638", "Calle 3 #8-99 San Fernando", "3 personas (2 niños, Prioridad #3)"),
    ("Jimmy Abal Bolaños", "0", "0", "Kilómetro 14 Alto Dapa callejón corazones verdes", "Prioridad #25"),
    ("Loirdy Julieth Florez", "0", "315 280 7593", "Parque del Pinar Torre 14", "12 personas (1 menor, Prioridad #56). Grietas expuestas en toda la torre"),
    ("Marilyn Flores Osorio", "0", "319 638 3366", "Calle 8N #10-18 B/ Bellavista", "2 personas (Prioridad #3). Grietas en fachada y daños estructurales"),
    ("Maria Nancy Orozco", "0", "321 589 0257", "Calle 4 Cra 14 #3A-32 Las Cruces", "1 adulto mayor, 3 niños (Prioridad #26). Techo cocina desprendido"),
    ("Jairo Vallejo", "0", "314 562 9762", "Calle 16 #1-118 Esquina B/ Fray Piña", "Prioridad #4. Poste expuesto y daños en fachada"),
    ("Zoraida Rivera Gomez", "0", "312 224 0593", "Cra 40 Oeste #1C-13 Pedregal", "5 personas (2 niños, Prioridad #13). Fachada inclinada, grietas y techo"),
    ("Luz Marleny Rodriguez", "0", "314 424 1080", "Cra 3CN #12 Las Vegas", "Casa 3 pisos, 2 niños (Prioridad #1). Grietas en diferentes áreas"),
    ("Maria Eufemia Ortiz Montez", "0", "0", "Cra 6N #9-31 B/ Lleras", "8 personas, persona con discapacidad - Mauricio Ortiz (Prioridad #5). Techo a punto de colapsar"),
    ("Martha Isabel Escobar", "0", "317 863 7734", "Cll 11 Noroeste #1AN-05 B/ Campestre Real", "Prioridad #15. Grietas y daños estructurales"),
    ("Jose Alonso Zuñiga", "0", "312 829 6467", "Cll 3 #14N-43 B/ Madrigal", "Adulto mayor con Alzheimer (Prioridad #2). Grietas y daños estructurales"),
    ("Rosalba Anacona", "0", "317 778 8435", "Carrera 15A #24-03 B/ La Estancia Vieja", "Prioridad #18. Grietas y averías estructurales"),
    ("Monela Cordoba Nieves", "0", "311 378 8350", "Calle 15A #13-57 Nueva Estancia", "Prioridad #18. Daños estructurales"),
    ("Isabel Carpe", "0", "311 741 5543", "Carrera 3D Norte Calle 1 Avesta B/ Filandia", "Torre 4 pisos, 50 personas (Prioridad #17). El edificio cede considerablemente"),
    ("Gabrel Hermon Alvarez", "0", "310 671 8901", "Calle 16 #12-10 B/ La Nueva Extensión", "Prioridad #18. Fisuras en pared, columna vuelta"),
    ("Maria de los Angeles Rodriguez", "0", "314 800 3465", "Cra 7 #14-45 Barrio Coorfandi", "Prioridad #33. Grietas en toda la casa"),
    ("Minom Urrea", "0", "311 756 0953", "Calle 12A #8-05 San Fernando", "Prioridad #50. Casa 2 niveles, fisura en parte baja de pared"),
    ("Henry Giovanny Betancourt", "0", "312 205 4901", "Cll 3 #69-95 San Fernando", "Prioridad #33. Grietas en muro de contención, pared a punto de caer"),
    ("Luisa Maria Diaz Muñoz", "1130591481", "312 644 3098", "Kra 18E #65-37 B/ Villa Esperanza", "2 personas (1 niño de 10 años). Habitan en sala por afectación en paredes y techo"),
    ("Margot Sanchez Patiño", "31982025", "302 252 9383", "Kra 13A #15B-04 B/ La Nueva Estancia", "2 adultos mayores. Columna cuarteada de lado a lado"),
    ("Ferney Rodriguez", "1118299615", "316 506 5676", "Cra 15A #8-16", "1 adulto. Muro de piedra de soporte derrumbado, hueco de 30cm en el piso"),
    ("Victor Manuel Arenas", "1118296910", "316 140 5870", "Calle 7 #16-149 Buenos Aires", "2 adultos, 1 menor. Grietas en paredes y caída de panel de yeso"),
    ("Saola Andrea Gonzales", "1118294583", "316 679 8104", "Cra 3 Noroeste #10-58 Trinidad Orilla del Río", "2 niños (1 con discapacidad), 1 adulto. Grietas en paredes"),
    ("Maria Nohelia Osorio Valdez", "24510850", "321 805 2836", "Calle 10 #17-01 B/ Las Américas", "La señora Nohelia y 1 hijo. Piso de sala agrietado, cielo raso caído, pared abombada"),
    ("Carolina Cucalón Risaralde", "1130675514", "315 511 4432", "Calle 5 #76-53 Edificio Veracna Apto 502", "2 adultos. Fisuras y grietas en paredes"),
    ("Ana Cecilia Montes", "31470393", "314 851 9833", "Calle Gase #4-04 B/ Nuevo Horizonte", "5 personas (2 adultos mayores). Piso agrietado en habitación, pared ladeada"),
    ("Juan Carlos Gil Gonzalez", "1005785242", "310 386 3096", "Carrera 9 #5AN-63 B/ Bellavista", "Madre adulta mayor con parálisis y silla de ruedas. Paredes de bahareque con recubrimiento desprendido"),
    ("Jhon Breiner Quintero Avila", "1006435779", "313 715 8791", "Calle 9A #13-105 B/ Buenos Aires", "2 adultos, 2 menores. Separación de pared con viga, casa inclinada con riesgo de colapso"),
    ("Hawi Alexis Tonuzco Salas", "1118292406", "302 203 1367", "Carrera 2 #2-179 Dionisio Calderón", "2 personas (hijo y adulta mayor). Grietas en paredes, piso levantado, desprendimiento en columna"),
    ("John Jairo Fernandez Fernandez", "16756173", "310 754 1923", "Calle 8 #8-25 B/ Uribe", "3 adultos. Casa 2 pisos con paredes del 1er piso y habitaciones del 2do piso averiadas"),
    ("Ana Milena Mesa Fajardo", "31969467", "311 389 8458", "Calle 70 con Kra 16 #1-5 Apto 102 B/ Panorama", "5 personas (1 menor de 10, 1 de 15). Pared de fachada con grieta en diagonal"),
    ("Fabiola Lora Luque", "0", "311 669 6821", "Dapa KM 2.85 Pistas de Dapa", "Solicitud general de insumos de emergencia")
]

def main():
    print("Iniciando inserción de solicitudes como reportes comunitarios...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        insertados = 0
        for s in SOLICITUDES:
            nombre, doc, tel, drc, detalles = s
            reporte_id = str(uuid.uuid4())
            titulo = f"Solicitud de Visita - {nombre} (Doc: {doc})"
            descripcion = f"Teléfono: {tel}. Detalles/Afectación: {detalles}"
            
            cur.execute("""
                INSERT INTO public.reportes_comunitarios 
                (id, titulo, descripcion_detallada, direccion_referencia, estado_actual, migrado_rufe, activo, gravedad)
                VALUES (%s, %s, %s, %s, 'Pendiente', false, true, 3);
            """, (reporte_id, titulo, descripcion, drc))
            insertados += 1

        print(f"\n==================================================")
        print(f"MIGRACIÓN EXITOSA. Total reportes creados en estado Pendiente: {insertados}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
