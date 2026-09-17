import psycopg2
import uuid
import re

DB_CONFIG = {
    "dbname": "comunidad_db",
    "user": "admin_comunidad",
    "password": "TuPasswordSegura2026!",
    "host": "10.147.17.24",
    "port": "5432"
}

LOTES_NUEVOS_RUFE = [
    {
        "num_formulario": "1061", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Watercol SAS - 11 a 50 empleados, laborando de manera parcial, pérdidas entre 20 y 100 millones (RDE-1061).",
        "personas": [{"nombre": "Watercol SAS", "doc": "901193743", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1062", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Alexander Soto Agudelo - 1 empleado, afectación menor en inventario (RDE-1062).",
        "personas": [{"nombre": "Alexander Soto Agudelo", "doc": "94475563", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1063", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Luz Alba Silva Delgado - Inmueble verificado sin información de afectación sísmica (RDE-1063).",
        "personas": [{"nombre": "Luz Alba Silva Delgado", "doc": "39714756", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1064", "corregimiento": "La Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Texhome / Juan Fernando - 11 a 50 empleados, daños en infraestructura y mercancía (RDE-1064).",
        "personas": [{"nombre": "Texhome", "doc": "1116268662", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1065", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Semillas del Valle - 51 a 200 trabajadores, pérdidas superiores a 100 millones (RDE-1065).",
        "personas": [{"nombre": "Semillas del Valle", "doc": "890306231", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1066", "corregimiento": "Cencar", "prioridad": "ALTA",
        "observaciones_evaluador": "Solo Camiones SAS - 6 a 10 trabajadores, daños en infraestructura y equipos, no puede operar (RDE-1066).",
        "personas": [{"nombre": "Solo Camiones SAS", "doc": "800150389", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1067", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jose Fabian Grisales Quintero - 2 a 5 trabajadores, afectación física y reducción de ventas (RDE-1067).",
        "personas": [{"nombre": "Jose Fabian Grisales Quintero", "doc": "1118292898", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1068", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Martha Lilian Galindo Navas - Inmueble con afectación moderada y requerimiento de reparaciones (RDE-1068).",
        "personas": [{"nombre": "Martha Lilian Galindo Navas", "doc": "65792357", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1069", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Federación de Empresas de Transporte - Pérdidas entre 5 y 20 millones, operación parcial (RDE-1069).",
        "personas": [{"nombre": "Federación de Empresas de Transporte", "doc": "800012149", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1070", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Global Agricultural Business - 11 a 50 trabajadores, pérdidas y afectación crítica (RDE-1070).",
        "personas": [{"nombre": "Global Agricultural Business", "doc": "901007263", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1071", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Industria Prosoy SAS - Operación normal, afectación emocional leve (RDE-1071).",
        "personas": [{"nombre": "Industria Prosoy SAS", "doc": "900344522", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1072", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Industria de Aluminios India - 11 a 50 trabajadores, pérdidas superiores a 100 millones (RDE-1072).",
        "personas": [{"nombre": "Industria de Aluminios India", "doc": "896308729", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1073", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Importfoods S.A.S. - 11 a 50 trabajadores, operación parcial (RDE-1073).",
        "personas": [{"nombre": "Importfoods S.A.S.", "doc": "901393197", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1074", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Invartrans R.G.M. - Operación normal, pérdidas menores a 5 millones (RDE-1074).",
        "personas": [{"nombre": "Invartrans R.G.M.", "doc": "9004267857", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1075", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Julio Cesar - 2 a 5 trabajadores, daños en infraestructura y equipos (RDE-1075).",
        "personas": [{"nombre": "Julio Cesar", "doc": "94384393", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1076", "corregimiento": "Dapa Miravalle", "prioridad": "MEDIA",
        "observaciones_evaluador": "Alberto Amaya Reyes - 2 a 5 trabajadores, operación parcial (RDE-1076).",
        "personas": [{"nombre": "Alberto Amaya Reyes", "doc": "19468985", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1077", "corregimiento": "Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Apoyos contra el Cáncer / Christian David Trujillo - 2 a 5 trabajadores, afectación grave (RDE-1077).",
        "personas": [{"nombre": "Apoyos contra el Cáncer", "doc": "901923364", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1078", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Alimentos Cárnicos S.A.S. - Más de 200 trabajadores, operación parcial (RDE-1078).",
        "personas": [{"nombre": "Alimentos Cárnicos S.A.S.", "doc": "890304130", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1079", "corregimiento": "Las Américas", "prioridad": "ALTA",
        "observaciones_evaluador": "Ana Milena Lerma - 1 a 5 trabajadores, no puede operar, afectación crítica (RDE-1079).",
        "personas": [{"nombre": "Ana Milena Lerma", "doc": "31488552", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1080", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Aluminio Nacional S.A.S. - Más de 200 trabajadores, operación normal (RDE-1080).",
        "personas": [{"nombre": "Aluminio Nacional S.A.S.", "doc": "890300213", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1081", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Amarunka Kombucha - 1 trabajador, inventarios afectados, operación parcial (RDE-1081).",
        "personas": [{"nombre": "Amarunka Kombucha", "doc": "1113652479", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1082", "corregimiento": "Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Diana Milena Buritica Mendoza - Inmueble con prioridad baja (RDE-1082).",
        "personas": [{"nombre": "Diana Milena Buritica Mendoza", "doc": "29975617", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1083", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "ACL Logística S.A. - Más de 200 trabajadores (RDE-1083).",
        "personas": [{"nombre": "ACL Logística S.A.", "doc": "900423131", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1084", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Agencia de Publicidad / Andrea Gomez - No puede operar, daños en infraestructura (RDE-1084).",
        "personas": [{"nombre": "Agencia de Publicidad", "doc": "1113537936", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1085", "corregimiento": "Acopi", "prioridad": "BAJA",
        "observaciones_evaluador": "Agro Integral Andina - Más de 200 trabajadores, operación normal (RDE-1085).",
        "personas": [{"nombre": "Agro Integral Andina", "doc": "860511458", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1086", "corregimiento": "Arroyohondo", "prioridad": "BAJA",
        "observaciones_evaluador": "STL Ibazar S.A.S. - Transporte de carga, operación normal (RDE-1086).",
        "personas": [{"nombre": "STL Ibazar S.A.S.", "doc": "9091132319", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1087", "corregimiento": "Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Servicasa Yumbo 2000 - Servicios administrativos, no puede operar (RDE-1087).",
        "personas": [{"nombre": "Servicasa Yumbo 2000", "doc": "91207637", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1088", "corregimiento": "Arroyohondo", "prioridad": "BAJA",
        "observaciones_evaluador": "Carpas IWF Cali S.A.S. - Operación normal, pérdidas menores a 5 millones (RDE-1088).",
        "personas": [{"nombre": "Carpas IWF Cali S.A.S.", "doc": "901308345", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1089", "corregimiento": "Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Monica Cardona Rodriguez - Entretenimiento, operación normal (RDE-1089).",
        "personas": [{"nombre": "Monica Cardona Rodriguez", "doc": "1118306067", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1090", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Elmar / Balanta Mina - 2 a 5 trabajadores, operación parcial (RDE-1090).",
        "personas": [{"nombre": "Elmar", "doc": "16464842", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1091", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Entrega S.A.S. - 11 a 50 trabajadores, afectación grave (RDE-1091).",
        "personas": [{"nombre": "Entrega S.A.S.", "doc": "805010341", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1092", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Dinámica Logística S.A.S. - 11 a 50 trabajadores, operación parcial (RDE-1092).",
        "personas": [{"nombre": "Dinámica Logística S.A.S.", "doc": "9000550294", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1093", "corregimiento": "Madrigal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Escobar Medina Maria Zuleima - 1 trabajador, microempresa (RDE-1093).",
        "personas": [{"nombre": "Maria Zuleima Escobar Medina", "doc": "1118287845", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1094", "corregimiento": "Buenos Aires", "prioridad": "BAJA",
        "observaciones_evaluador": "Tienda Galera / Dolfy Falsory - Operación normal (RDE-1094).",
        "personas": [{"nombre": "Dolfy Falsory", "doc": "1067465647", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1095", "corregimiento": "Arroyohondo", "prioridad": "MEDIA",
        "observaciones_evaluador": "15cm 106center S.A.S. - Inventarios afectados, pérdidas entre 5 y 20 millones (RDE-1095).",
        "personas": [{"nombre": "15cm 106center S.A.S.", "doc": "901474130", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1096", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "TIKI bar - Alojamiento y comida, pérdidas menores a 5 millones (RDE-1096).",
        "personas": [{"nombre": "TIKI bar", "doc": "1118290464", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1097", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Toning S.A.S. - Daños en infraestructura y maquinaria, operación parcial (RDE-1097).",
        "personas": [{"nombre": "Toning S.A.S.", "doc": "891303109", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1098", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Transportes Camiones Ltda. - Operación parcial, pérdidas entre 5 y 20 millones (RDE-1098).",
        "personas": [{"nombre": "Transportes Camiones Ltda.", "doc": "805027046", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1099", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Servi-Grafic S.A.S. - 51 a 200 trabajadores, daños graves (RDE-1099).",
        "personas": [{"nombre": "Servi-Grafic S.A.S.", "doc": "890300228", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1100", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Tableros Eléctricos S.A.S. - Pérdidas superiores a 100 millones, no puede operar (RDE-1100).",
        "personas": [{"nombre": "Tableros Eléctricos S.A.S.", "doc": "800093443", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1101", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Asociación de Mujeres - Servicios generales (RDE-1101).",
        "personas": [{"nombre": "Asociación de Mujeres", "doc": "805014770", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1102", "corregimiento": "La Laguna", "prioridad": "MODERADA",
        "observaciones_evaluador": "David Alexander Beltran Baonza - Alojamiento y comida, pérdidas entre 5 y 20 millones (RDE-1102).",
        "personas": [{"nombre": "David Alexander Beltran Baonza", "doc": "1144187942", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1103", "corregimiento": "Rincón Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Salsabor / Juan David Ordoñez - 1 trabajador, afectación baja (RDE-1103).",
        "personas": [{"nombre": "Salsabor", "doc": "1193125111", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1104", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Brújula Trips S.A.S. - 51 a 200 trabajadores, operación parcial (RDE-1104).",
        "personas": [{"nombre": "Brújula Trips S.A.S.", "doc": "901555159", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1105", "corregimiento": "Las Américas", "prioridad": "ALTA",
        "observaciones_evaluador": "Dolly Benjumea Marrongo - Alojamiento y comida, no puede operar (RDE-1105).",
        "personas": [{"nombre": "Dolly Benjumea Marrongo", "doc": "1118290857", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1106", "corregimiento": "Belalcázar", "prioridad": "BAJA",
        "observaciones_evaluador": "Yumbo Seguros Generales Colombia - Verificado sin observaciones (RDE-1106).",
        "personas": [{"nombre": "Yumbo Seguros Generales Colombia", "doc": "66773448", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1107", "corregimiento": "Mirador Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Queteria Venta de Espejos - Inmueble verificado (RDE-1107).",
        "personas": [{"nombre": "Yeison Garcia", "doc": "1118299249", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1108", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Codas Amigos S.A.S. - Sin daños en infraestructura (RDE-1108).",
        "personas": [{"nombre": "Codas Amigos S.A.S.", "doc": "1118308307", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1109", "corregimiento": "Fray Peña", "prioridad": "ALTA",
        "observaciones_evaluador": "La Mona de Yumbo - Daños en infraestructura (paredes, baños, techo) (RDE-1109).",
        "personas": [{"nombre": "La Mona de Yumbo", "doc": "1006337700", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1110", "corregimiento": "Rincón Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Boutique Bar Shop - Inmueble comercial verificado (RDE-1110).",
        "personas": [{"nombre": "Boutique Bar Shop", "doc": "31323688", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    }
]

def obtener_grupo_poblacional(edad):
    if edad is None: return "Sin Registro"
    if edad <= 14: return "1. Primera Infancia y Niños (0-14)"
    elif edad <= 28: return "2. Jóvenes (15-28)"
    elif edad <= 59: return "3. Adultos (29-59)"
    else: return "4. Adultos Mayores (60+)"

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match: return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1061-1110...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        cur.execute("ALTER TABLE public.rufe_personas ADD COLUMN IF NOT EXISTS grupo_poblacional VARCHAR(50);")
        
        formularios_creados, formularios_actualizados = 0, 0
        personas_creadas, personas_actualizadas = 0, 0
        
        cur.execute("SELECT id FROM public.reportes_comunitarios LIMIT 1;")
        res_reporte = cur.fetchone()
        
        if not res_reporte:
            reporte_id = str(uuid.uuid4())
            cur.execute("INSERT INTO public.reportes_comunitarios (id, activo) VALUES (%s, true) ON CONFLICT DO NOTHING;", (reporte_id,))
        else:
            reporte_id = res_reporte[0]
            
        for form in LOTES_NUEVOS_RUFE:
            num_limpio = form["num_formulario"].lstrip('0')
            
            cur.execute("SELECT id FROM public.rufe_formularios WHERE numero_formulario = %s", (num_limpio,))
            resultado = cur.fetchone()
            
            if resultado:
                form_id = resultado[0]
                cur.execute("""
                    UPDATE public.rufe_formularios 
                    SET prioridad = %s, observaciones_evaluador = %s WHERE id = %s;
                """, (form["prioridad"], form["observaciones_evaluador"], form_id))
                formularios_actualizados += 1
            else:
                cur.execute("""
                    INSERT INTO public.rufe_formularios 
                    (reporte_id, numero_formulario, corregimiento, prioridad, observaciones_evaluador)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (reporte_id, num_limpio, form["corregimiento"], form["prioridad"], form["observaciones_evaluador"]))
                form_id = cur.fetchone()[0]
                formularios_creados += 1
                
            for p in form["personas"]:
                if p["doc"] == "0": continue
                edad_calc = calcular_edad_2026(p["fecha"])
                grupo_pob = obtener_grupo_poblacional(edad_calc)
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE REPLACE(documento_identidad, '.', '') = %s", (p["doc"],))
                res_persona = cur.fetchone()
                
                if res_persona:
                    persona_id = res_persona[0]
                    cur.execute("""
                        UPDATE public.rufe_personas 
                        SET fecha_nacimiento = %s, edad = %s, es_jefe_hogar = %s, parentesco = %s, sexo = %s, etnia = %s, grupo_poblacional = %s
                        WHERE id = %s;
                    """, (p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], grupo_pob, persona_id))
                    personas_actualizadas += 1
                else:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, edad, es_jefe_hogar, parentesco, sexo, etnia, grupo_poblacional)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (form_id, p["nombre"], p["doc"], p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], grupo_pob))
                    personas_creadas += 1

        print(f"\n==================================================")
        print(f"MIGRACIÓN LOTE 1061-1110 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
