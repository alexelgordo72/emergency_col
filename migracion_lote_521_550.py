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
        "num_formulario": "521", "corregimiento": "Buitrera Centro", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda sin sistema estructural, con deslizamiento en pasillos que comprometen la estabilidad del bien.",
        "personas": [
            {"nombre": "Leonardo Alberto Dolmar Londoño", "doc": "16692147", "fecha": "26/04/1996", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Julio Cesar Sanchez Ortiz", "doc": "16821879", "fecha": "01/01/1960", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "522", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con afectaciones graves en mampostería y estructura.",
        "personas": [
            {"nombre": "Jorge Yarpaz", "doc": "6341067", "fecha": "19/03/1960", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Argenis Ortiz Gomez", "doc": "0", "fecha": "01/01/1963", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "523", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Cubierta averiada.",
        "personas": [
            {"nombre": "Emilia Ortiz", "doc": "31478650", "fecha": "24/04/1946", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "524", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque con muros colapsados y soportes debilitados.",
        "personas": [
            {"nombre": "Eloiza Erazo", "doc": "31895118", "fecha": "15/08/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "525", "corregimiento": "Buitrera Centro", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material con mampostería afectada en un 80% y refuerzo en viga de amarre necesario.",
        "personas": [
            {"nombre": "Martha Lucia Garcia Lopez", "doc": "41430121", "fecha": "19/11/1948", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Heric Rojas", "doc": "19066097", "fecha": "24/02/1949", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Erick Rojas Garcia", "doc": "79784521", "fecha": "01/12/1975", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "526", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Mampostería comprometida en un 80% con riesgo de colapso.",
        "personas": [
            {"nombre": "Samuel Benavidez", "doc": "16453463", "fecha": "29/07/1966", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carliña Ortiz", "doc": "631475088", "fecha": "01/01/1970", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "527", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con fracturas importantes en columnas y desprendimiento de pañete en área de cocina.",
        "personas": [
            {"nombre": "Jose Luis Ortiz", "doc": "2693438", "fecha": "01/01/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Erlinda Araujo", "doc": "31478085", "fecha": "01/01/1968", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "528", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con afectaciones en mampostería en un 80% y 2 columnas con fracturas considerables.",
        "personas": [
            {"nombre": "Fernando Pablo Hidalgo", "doc": "94379110", "fecha": "19/01/1971", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "529", "corregimiento": "Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de dos pisos con fisuras leves en mampostería. Habitable.",
        "personas": [
            {"nombre": "Olga Gutierrez", "doc": "29980191", "fecha": "09/05/1949", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Natalia Gutierrez", "doc": "1001349780", "fecha": "22/10/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Nicol Dayana Avila", "doc": "1030638086", "fecha": "29/02/2012", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "530", "corregimiento": "Buitrera", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en bahareque colapsada parcialmente. Se recomienda remodelación.",
        "personas": [
            {"nombre": "Francia Elena Chanchi Hoyos", "doc": "31485039", "fecha": "24/04/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gabriela Rengifos Chanchi", "doc": "1107868226", "fecha": "12/10/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "531", "corregimiento": "Buitrera Centro", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda destruida por sismo.",
        "personas": [
            {"nombre": "Edinson Esteban Hoyos", "doc": "1118292214", "fecha": "27/08/1989", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gabriela Cardenas C.", "doc": "1118311770", "fecha": "22/08/1999", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "532", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con mampostería afectada en un 80% con sistema estructural deficiente y colapsado en un 40%.",
        "personas": [
            {"nombre": "Edwin Alfredo Aguirre", "doc": "94506859", "fecha": "14/08/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Elver Aguilon Lopez", "doc": "16453998", "fecha": "01/01/1971", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "533", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con mampostería averiada sin sistema estructural y muro colapsado. Integrante con discapacidad (mudo-NN).",
        "personas": [
            {"nombre": "Angelita del Socorro Martinez", "doc": "66904296", "fecha": "19/05/1971", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "534", "corregimiento": "La Paz", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda destruida.",
        "personas": [
            {"nombre": "Liceth Fernanda Rengifo", "doc": "14941659", "fecha": "01/01/1983", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Edgar Rengifo Rengifo", "doc": "1118288157", "fecha": "04/01/1986", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Xomara Ancopa R.", "doc": "1105381077", "fecha": "25/10/2011", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Antonio Ancopa R.", "doc": "4539102", "fecha": "01/04/1982", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Lina Maria Rengifo", "doc": "1107055820", "fecha": "04/05/1988", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Felipe Buitron", "doc": "87249417", "fecha": "01/01/1985", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "535", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con mampostería afectada en un 80%. Refuerzo en viga de amarre.",
        "personas": [
            {"nombre": "Martha Lucia Garcia Lopez", "doc": "41430121", "fecha": "19/11/1948", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Heric Rojas", "doc": "19066097", "fecha": "24/02/1949", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Erick Rojas Garcia", "doc": "79784521", "fecha": "01/12/1975", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "536", "corregimiento": "Rincon Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mampostería debilitada con riesgo de colapso, afectada en un 30%.",
        "personas": [
            {"nombre": "Diego Hernan Inga Velasco", "doc": "1118292636", "fecha": "12/05/1989", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Edilana Johana Ceron Muñoz", "doc": "1019360405", "fecha": "30/12/1990", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Sara Valentina Inga Ceron", "doc": "11485622", "fecha": "18/07/2015", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "537", "corregimiento": "Buitrera Centro", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras leves en mampostería, algunos asentamientos en pasillos (reparables).",
        "personas": [
            {"nombre": "Juan Martin Garcia", "doc": "419179258", "fecha": "01/01/1963", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sandra Garcia", "doc": "10949215548", "fecha": "01/01/1969", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Sebastian Restrepo", "doc": "7526542", "fecha": "16/07/1991", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Olmedo Restrepo", "doc": "41900594", "fecha": "01/01/1958", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Aida Garcia", "doc": "7541517", "fecha": "01/01/1963", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "538", "corregimiento": "Buitrera Centro", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras leves en mampostería. Sistema estructural en perfectas condiciones.",
        "personas": [
            {"nombre": "Teodoro Pipicano Lopez", "doc": "6341911", "fecha": "17/09/1986", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Lilia Tovar", "doc": "29581802", "fecha": "01/06/1987", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "539", "corregimiento": "Buitrera El Crucero", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras en juntas de muro y desprendimiento de recubrimiento en mampostería y vigas.",
        "personas": [
            {"nombre": "Rafael Ramirez", "doc": "1636040", "fecha": "28/08/1934", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ludivia Posada", "doc": "31465336", "fecha": "24/01/1954", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "540", "corregimiento": "Buitrera Las Lomitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con afectación por colapso parcial de muro ciclópeo cedido por talud.",
        "personas": [
            {"nombre": "Maria Aide Bernal", "doc": "16753755", "fecha": "16/10/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cesar Augusto Lopez", "doc": "31984204", "fecha": "20/10/1968", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Elsa Marina Lopez Bernal", "doc": "0", "fecha": "29/02/1965", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "541", "corregimiento": "Rincon Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con afectaciones mínimas en mampostería.",
        "personas": [
            {"nombre": "Doris Lucia Ordoñez", "doc": "66854988", "fecha": "12/02/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luis Alirio Burbano", "doc": "31478022", "fecha": "05/05/1965", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "542", "corregimiento": "Buitrera Centro", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras en mampostería, sistema estructural en perfectas condiciones.",
        "personas": [
            {"nombre": "Rodrigo Mateus", "doc": "19290148", "fecha": "09/08/1955", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Bellaneth Ordoñez Cardenas", "doc": "66731933", "fecha": "28/07/1967", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Rosalba Cardenas", "doc": "31371193", "fecha": "29/10/1943", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "544", "corregimiento": "Dapa El Chocho", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con averías en mampostería reparables. Sistema estructural visualmente bien.",
        "personas": [
            {"nombre": "Maria del Pilar Montalvo Zarama", "doc": "31861268", "fecha": "21/03/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juan Francisco Suarez Montalvo", "doc": "1107083913", "fecha": "04/10/1993", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "545", "corregimiento": "La Paz Perez", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras menores y talud de tierra con desplazamiento.",
        "personas": [
            {"nombre": "Alejandro Cantor Caballero", "doc": "60261064", "fecha": "29/01/1983", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Laneninl Caballero Cantor", "doc": "14698566", "fecha": "23/06/1976", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Nayarith Cantor Caballero", "doc": "1093434366", "fecha": "18/12/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "David Alejandro Cantor Caballero", "doc": "1093435222", "fecha": "19/06/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "546", "corregimiento": "Miravalle Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras leves en mampostería.",
        "personas": [
            {"nombre": "Andres Felipe Pasaje Gomez", "doc": "1080266173", "fecha": "05/03/2016", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Emely Valentina Pasaje Gomez", "doc": "1145825828", "fecha": "16/06/2010", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Dromelina Chavaco", "doc": "71489651", "fecha": "13/01/1952", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "547", "corregimiento": "Dapa Paraiso", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda estructuralmente estable, leves fisuras en mampostería.",
        "personas": [
            {"nombre": "Jorge Hector Orjón Ospina", "doc": "5921016", "fecha": "16/01/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Emma Preciado", "doc": "28756455", "fecha": "07/11/1946", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Sandra Liliana Ospina Preciado", "doc": "31478401", "fecha": "18/10/2000", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "548", "corregimiento": "Buitrera La Esperanza", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con fisuras y desprendimiento de revestimiento en muros.",
        "personas": [
            {"nombre": "Francia Elena Buitrago Cardenas", "doc": "1118292214", "fecha": "26/02/1999", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jenny Liliana Guzman", "doc": "1148303438", "fecha": "21/05/1994", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "549", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Reparaciones locativas en mampostería y confinamiento para cuarto.",
        "personas": [
            {"nombre": "Mirlan Bernal", "doc": "51693523", "fecha": "10/02/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "550", "corregimiento": "Miravalle El Chocho", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras menores en mampostería y sistema estructural resistente.",
        "personas": [
            {"nombre": "Robinson Mesa", "doc": "94397033", "fecha": "03/06/1973", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andrea Paola Mesa Gomez", "doc": "1118289672", "fecha": "25/06/1988", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Angie Lucia Mesa Gomez", "doc": "1109185146", "fecha": "01/10/2004", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Laura Sofia Mesa Gomez", "doc": "1109190937", "fecha": "15/10/2008", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Mariana Andrea Mesa Guerrero", "doc": "1109194134", "fecha": "14/02/2013", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ismael David Mesa Guerrero", "doc": "1109940595", "fecha": "18/07/2026", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
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
    print("Iniciando ENRIQUECIMIENTO Lote 521-550...")
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
        print(f"MIGRACIÓN LOTE 521-550 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
