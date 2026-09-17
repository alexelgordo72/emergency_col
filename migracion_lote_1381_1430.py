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
        "num_formulario": "1381", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Comercial de aluminios y vidrios espinosa - Nivel de afectación moderada (RDE-1381).",
        "personas": [{"nombre": "Comercial de aluminios y vidrios espinosa", "doc": "6531265", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1382", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Junta Administradora de acueducto y alcantarillado del corregimiento de San Marcos (aasanm) - Nivel de afectación crítica (RDE-1382).",
        "personas": [{"nombre": "Aasanm", "doc": "90036709", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1383", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Galindo Nieves Martha Lilian - Nivel de afectación moderada (RDE-1383).",
        "personas": [{"nombre": "Martha Lilian Galindo Nieves", "doc": "65792357", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1384", "corregimiento": "Cencar", "prioridad": "ALTA",
        "observaciones_evaluador": "Transportes Camiones y Camiones Ltda - Nivel de afectación grave (RDE-1384).",
        "personas": [{"nombre": "Transportes Camiones y Camiones Ltda", "doc": "805027046", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1385", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "WM Impresores S.A. - Nivel de afectación grave (RDE-1385).",
        "personas": [{"nombre": "WM Impresores S.A.", "doc": "805001509", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1386", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Lazyamor - Nivel de afectación grave (RDE-1386).",
        "personas": [{"nombre": "Lazyamor", "doc": "25292899", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1387", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Ussa Garcia Rodolfo - Nivel de afectación moderada (RDE-1387).",
        "personas": [{"nombre": "Rodolfo Ussa Garcia", "doc": "94468438", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1388", "corregimiento": "Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Apoyos contra el Cáncer S.A.S. - Nivel de afectación grave (RDE-1388).",
        "personas": [{"nombre": "Apoyos contra el Cáncer S.A.S.", "doc": "901923364", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1389", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Mayorga Mahecha Fernando Leon - Sin clasificación (RDE-1389).",
        "personas": [{"nombre": "Fernando Leon Mayorga Mahecha", "doc": "94379771", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1390", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Turistrans SAS - Nivel de afectación crítica (RDE-1390).",
        "personas": [{"nombre": "Turistrans SAS", "doc": "4345559", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1391", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Industrias Prosoy S.A.S. - Nivel de afectación baja (RDE-1391).",
        "personas": [{"nombre": "Industrias Prosoy S.A.S.", "doc": "900344522", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1392", "corregimiento": "Las Américas", "prioridad": "ALTA",
        "observaciones_evaluador": "Benjumba Mairongo Dolly - Nivel de afectación crítica (RDE-1392).",
        "personas": [{"nombre": "Dolly Benjumba Mairongo", "doc": "1118290857", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1393", "corregimiento": "Arroyohondo", "prioridad": "MEDIA",
        "observaciones_evaluador": "SCM Logcenter SAS - Nivel de afectación moderada (RDE-1393).",
        "personas": [{"nombre": "SCM Logcenter SAS", "doc": "901474130", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1394", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Centro de eventos y hostelería Casablanca - Nivel de afectación crítica (RDE-1394).",
        "personas": [{"nombre": "Casablanca", "doc": "79040900", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1395", "corregimiento": "Cencar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Pulido Mesa Alejandro - Nivel de afectación moderada (RDE-1395).",
        "personas": [{"nombre": "Alejandro Pulido Mesa", "doc": "7225910", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1396", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Clay S.A. - Nivel de afectación grave (RDE-1396).",
        "personas": [{"nombre": "Clay S.A.", "doc": "805016105", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1397", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Villani Maldonado Ziomara - Nivel de afectación moderada (RDE-1397).",
        "personas": [{"nombre": "Ziomara Villani Maldonado", "doc": "1144201246", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1398", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Distribuidora de Suministros S.A.S. - Nivel de afectación crítica (RDE-1398).",
        "personas": [{"nombre": "Distribuidora de Suministros S.A.S.", "doc": "830111877", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1399", "corregimiento": "Miravalle Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Para Hombres S.A.S. - Nivel de afectación grave (RDE-1399).",
        "personas": [{"nombre": "Para Hombres S.A.S.", "doc": "800159974", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1400", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Entregas SAS - Nivel de afectación grave (RDE-1400).",
        "personas": [{"nombre": "Entregas SAS", "doc": "805010341", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1401", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Multi Ideas SAS - Nivel de afectación moderada (RDE-1401).",
        "personas": [{"nombre": "Multi Ideas SAS", "doc": "805015345", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1402", "corregimiento": "Buenos Aires", "prioridad": "BAJA",
        "observaciones_evaluador": "Tienda Galera Buenos Aires - Sin clasificación (RDE-1402).",
        "personas": [{"nombre": "Tienda Galera Buenos Aires", "doc": "1067465647", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1403", "corregimiento": "Cencar", "prioridad": "ALTA",
        "observaciones_evaluador": "Solo Camiones S.A.S. - Nivel de afectación crítica (RDE-1403).",
        "personas": [{"nombre": "Solo Camiones S.A.S.", "doc": "800150389", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1404", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Semillas Valle SA - Nivel de afectación grave (RDE-1404).",
        "personas": [{"nombre": "Semillas Valle SA", "doc": "890306231", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1405", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Industria de Aluminio India S.A.S. - Nivel de afectación crítica (RDE-1405).",
        "personas": [{"nombre": "Industria de Aluminio India S.A.S.", "doc": "896308729", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1406", "corregimiento": "Cencar", "prioridad": "GRAVE",
        "observaciones_evaluador": "Dinámica Logística S.A.S. - Nivel de afectación grave (RDE-1406).",
        "personas": [{"nombre": "Dinámica Logística S.A.S.", "doc": "9000550294", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1407", "corregimiento": "Prados del Limón", "prioridad": "BAJA",
        "observaciones_evaluador": "Lince Comercial S.A.S. - Sin clasificación (RDE-1407).",
        "personas": [{"nombre": "Lince Comercial S.A.S.", "doc": "805024696", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1408", "corregimiento": "Cencar", "prioridad": "ALTA",
        "observaciones_evaluador": "Federación de Empresas Transportadoras de Carga de Colombia - Nivel de afectación grave (RDE-1408).",
        "personas": [{"nombre": "Federación de Empresas Transportadoras de Carga", "doc": "800012149", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1409", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Importfoods S.A.S. - Nivel de afectación crítica (RDE-1409).",
        "personas": [{"nombre": "Importfoods S.A.S.", "doc": "901393197", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1410", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Orozco Durango Diana Maria - Sin clasificación (RDE-1410).",
        "personas": [{"nombre": "Diana Maria Orozco Durango", "doc": "1073820764", "fecha": "01/01/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1411", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Invertrans RGM - Nivel de afectación moderada (RDE-1411).",
        "personas": [{"nombre": "Invertrans RGM", "doc": "9004267857", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1412", "corregimiento": "Madrigal", "prioridad": "BAJA",
        "observaciones_evaluador": "Escobar Medina Maria Zuleima - Sin clasificación (RDE-1412).",
        "personas": [{"nombre": "Maria Zuleima Escobar Medina", "doc": "1118287845", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1413", "corregimiento": "Panorama", "prioridad": "ALTA",
        "observaciones_evaluador": "Lasagnas y Postres Jhoal - Nivel de afectación grave (RDE-1413).",
        "personas": [{"nombre": "Lasagnas y Postres Jhoal", "doc": "1118298713", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1414", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Silva Delgado Luz Alba - Sin clasificación (RDE-1414).",
        "personas": [{"nombre": "Luz Alba Silva Delgado", "doc": "39714756", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1415", "corregimiento": "Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Restaurante La Casona Dapa - Sin clasificación (RDE-1415).",
        "personas": [{"nombre": "Restaurante La Casona Dapa", "doc": "6136937", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1416", "corregimiento": "Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Pino Soto Claudia Lorena - Nivel de afectación grave (RDE-1416).",
        "personas": [{"nombre": "Claudia Lorena Pino Soto", "doc": "1007521945", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1417", "corregimiento": "Belalcázar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Zuñiga Calvache Aura Myriam - Nivel de afectación moderada (RDE-1417).",
        "personas": [{"nombre": "Aura Myriam Zuñiga Calvache", "doc": "34639087", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1418", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Global Agricultural Business S.A.S. - Nivel de afectación crítica (RDE-1418).",
        "personas": [{"nombre": "Global Agricultural Business S.A.S.", "doc": "901007263", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1419", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Conde Murillo Edie Yilmer - Nivel de afectación moderada (RDE-1419).",
        "personas": [{"nombre": "Edie Yilmer Conde Murillo", "doc": "16637234", "fecha": "01/01/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1420", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Centro Medico de Yumbo Limitada - Nivel de afectación moderada (RDE-1420).",
        "personas": [{"nombre": "Centro Medico de Yumbo Limitada", "doc": "800189588", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1421", "corregimiento": "Ciudad Guabinas", "prioridad": "BAJA",
        "observaciones_evaluador": "Equipos, Proyectos y Mantenimientos SAS - Sin clasificación (RDE-1421).",
        "personas": [{"nombre": "Equipos, Proyectos y Mantenimientos SAS", "doc": "901087847", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1422", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grupo It Global S.A.S. - Nivel de afectación moderada (RDE-1422).",
        "personas": [{"nombre": "Grupo It Global S.A.S.", "doc": "890302180", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1423", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Distribuidora la Costa S.A. - Nivel de afectación grave (RDE-1423).",
        "personas": [{"nombre": "Distribuidora la Costa S.A.", "doc": "805010752", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1424", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Menshen Colombia S.A.S. - Nivel de afectación crítica (RDE-1424).",
        "personas": [{"nombre": "Menshen Colombia S.A.S.", "doc": "901506103", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1425", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Giraldo Giraldo Jose Orlando - Nivel de afectación crítica (RDE-1425).",
        "personas": [{"nombre": "Jose Orlando Giraldo Giraldo", "doc": "70825694", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1426", "corregimiento": "Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Fundación Nazlyn Comunitaria - Nivel de afectación grave (RDE-1426).",
        "personas": [{"nombre": "Fundación Nazlyn Comunitaria", "doc": "901432670", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1427", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Soto Agudelo Alexander - Nivel de afectación moderada (RDE-1427).",
        "personas": [{"nombre": "Alexander Soto Agudelo", "doc": "94475563", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1428", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Texhome - Sin clasificación (RDE-1428).",
        "personas": [{"nombre": "Texhome", "doc": "1116268662", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1429", "corregimiento": "Acopi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Bituvial SAS - Nivel de afectación moderada (RDE-1429).",
        "personas": [{"nombre": "Bituvial SAS", "doc": "900531654", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1430", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Asociación de las micro, mediana empresas seccional valle del cauca - Nivel de afectación grave (RDE-1430).",
        "personas": [{"nombre": "Asociación Micro y Medianas Empresas Valle", "doc": "890300228", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1381-1430...")
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
        print(f"MIGRACIÓN LOTE 1381-1430 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
