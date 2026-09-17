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
        "num_formulario": "782", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con mampostería comprometida en un 80%, sistema estructural con columnas afectadas y hierros a la vista[cite: 53].",
        "personas": [
            {"nombre": "Luis Eugenio Echeverry C.", "doc": "16446001", "fecha": "28/07/1957", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "783", "corregimiento": "Buitrera Parte Alta", "prioridad": "ALTA",
        "observaciones_evaluador": "Sistema estructural colapsado y daños graves en mampostería en un 80%[cite: 53].",
        "personas": [
            {"nombre": "Mauricio Chahin", "doc": "91205180", "fecha": "12/05/1960", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sandra Zambrano Durán", "doc": "29533290", "fecha": "01/01/1965", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Jacob Chahin Zambrano", "doc": "1108639767", "fecha": "22/09/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "784", "corregimiento": "Dapa Rodadero", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda sin sistema estructural definido, mampostería afectada en un 85% y asentamientos[cite: 53].",
        "personas": [
            {"nombre": "Hedny Astaiza Samboni", "doc": "31474458", "fecha": "12/11/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "785", "corregimiento": "Dapa Rodadero", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en madera con riesgo de colapso inminente[cite: 53].",
        "personas": [
            {"nombre": "Leslie Ortiz Muñoz", "doc": "1113680062", "fecha": "22/01/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Segundo Ortiz Arcos", "doc": "16623503", "fecha": "01/11/1955", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"},
            {"nombre": "Emanuel Isaac Navia Ortiz", "doc": "1105935345", "fecha": "03/11/2019", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "786", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con desplazamiento y asentamientos importantes en el talud[cite: 54].",
        "personas": [
            {"nombre": "Maria Gnaan Arcos Guzman", "doc": "27450775", "fecha": "27/05/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Aldemar Antonio Muñoz Tovar", "doc": "3002850705", "fecha": "08/10/1972", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "787", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Casa de la iglesia con muros que presentan riesgo de desplazamiento y colapso[cite: 54].",
        "personas": [
            {"nombre": "Oscar Carton Prado", "doc": "16449911", "fecha": "11/03/1953", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alba Mirella Noguera", "doc": "29580758", "fecha": "12/10/1937", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "788", "corregimiento": "Rincon Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con desplazamientos y asentamientos en terreno y estructura[cite: 54].",
        "personas": [
            {"nombre": "Lesiardo Muñoz", "doc": "98322571", "fecha": "08/12/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "789", "corregimiento": "Rincon Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con construcciones menores sobre terreno inestable y desplazado[cite: 54].",
        "personas": [
            {"nombre": "Natalia Diaz Arcos", "doc": "38559889", "fecha": "08/03/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "790", "corregimiento": "Rincon Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con averías menores construida sobre terreno inestable y desplazado[cite: 54].",
        "personas": [
            {"nombre": "Yarp Morales Gomez", "doc": "1118304128", "fecha": "11/03/1995", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Karen Tatiana Gomez Arcos", "doc": "1107059099", "fecha": "29/11/1989", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Shaday Ordoñez Arcos", "doc": "1104030158", "fecha": "14/03/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "791", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con averías en mampostería sobre terreno inestable por desprendimiento y asentamientos[cite: 55].",
        "personas": [
            {"nombre": "Jorge Hector Ospina", "doc": "1118286028", "fecha": "27/03/1999", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yusmin Andrea Muñoz", "doc": "27974103", "fecha": "10/12/1984", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Hanna Jacobo Ospina Muñoz", "doc": "1109937340", "fecha": "29/05/2018", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Yusmin Andrea Ospina Muñoz", "doc": "1109927562", "fecha": "06/12/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "792", "corregimiento": "Dapa Rodadero", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en adobe con muros agrietados a punto de colapsar, sin sistema estructural definido[cite: 55].",
        "personas": [
            {"nombre": "Marniela Lopez Arango", "doc": "29971913", "fecha": "16/10/1946", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alixon Mathias Dominguez", "doc": "1118304899", "fecha": "20/10/2018", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Maria Emperatriz Mayorga Lopez", "doc": "31472973", "fecha": "19/03/1967", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "793", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda estructuralmente estable, talud en riesgo de colapso y desprendimiento en masa[cite: 55].",
        "personas": [
            {"nombre": "Jose Fernando Montoya Muñoz", "doc": "94265889", "fecha": "24/07/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Maria Muñoz", "doc": "38643729", "fecha": "08/11/1989", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Xiomara Montoya Muñoz", "doc": "1109547964", "fecha": "18/07/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "794", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de bahareque con desplome parcial de cubierta de zinc y madera, muros perimetrales con desplome y riesgo de colapso[cite: 55].",
        "personas": [
            {"nombre": "Socorro Juanita Arcos Guzman", "doc": "27451421", "fecha": "14/07/1971", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juan Diego Lemos Arcos", "doc": "1109184589", "fecha": "01/06/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "795", "corregimiento": "Dapa Miravalle", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con sistema estructural destruido, alto riesgo de colapso[cite: 55].",
        "personas": [
            {"nombre": "Diego Fernando Salazar Ocampo", "doc": "94513520", "fecha": "21/01/1978", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ines Lorena Ospina Garcia", "doc": "29820760", "fecha": "30/10/1980", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Gloria Isabel Ocampo de Salazar", "doc": "0", "fecha": "21/04/1957", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "796", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda sin sistema estructural, mampostería no confinada y colapsada[cite: 56].",
        "personas": [
            {"nombre": "Diego Enrique Castillo", "doc": "6342952", "fecha": "14/12/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Neider Posso", "doc": "38894138", "fecha": "20/07/1974", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "797", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con mampostería afectada y sistema estructural con fisuras y grietas por desprendimiento[cite: 56].",
        "personas": [
            {"nombre": "Avila Muñoz Cruz", "doc": "27457404", "fecha": "12/04/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Margarita Bolaños", "doc": "1006037653", "fecha": "22/05/2001", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "798", "corregimiento": "Dapa Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Apartamento 103 Torre 19A Hacienda Verde, fisuras leves, se sugiere revisión de plaquetas de carga[cite: 56].",
        "personas": [
            {"nombre": "Edelmo Muñoz", "doc": "1004536582", "fecha": "28/10/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "799", "corregimiento": "Dapa Panorama", "prioridad": "ALTA",
        "observaciones_evaluador": "Edificación con daños estructurales evaluados por profesional[cite: 56].",
        "personas": [
            {"nombre": "Sara Buitica", "doc": "1023875224", "fecha": "30/11/1987", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yeo Dan Melendez", "doc": "83241953", "fecha": "07/07/1982", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Sergio Andres Cuervo", "doc": "102919765", "fecha": "26/06/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jesica Mildre Melendez", "doc": "1080264558", "fecha": "03/06/2013", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "800", "corregimiento": "Arroyohondo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Caballete y teja en mal estado, daños en solar sin ayudas previas[cite: 56].",
        "personas": [
            {"nombre": "Maria Chirimuscay", "doc": "1118306477", "fecha": "14/08/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jhonatan Rivera", "doc": "1139837370", "fecha": "10/10/2018", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Plinio Chirimuscay", "doc": "10751432", "fecha": "13/11/1961", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "801", "corregimiento": "Guadalupe", "prioridad": "BAJA",
        "observaciones_evaluador": "Caída de muros en marraneras[cite: 57].",
        "personas": [
            {"nombre": "Elka Mary Moreno Riascos", "doc": "29940771", "fecha": "17/09/1954", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Mulanda Rocio Meneses Ruiz", "doc": "31465354", "fecha": "24/09/1973", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Blanca Elsy Ruiz Meneses", "doc": "1006016906", "fecha": "19/07/1974", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "802", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Grietas en muros[cite: 57].",
        "personas": [
            {"nombre": "Blanca Mery Riascos Moreno", "doc": "31465354", "fecha": "07/09/1954", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Laura Marcela Meneses Moreno", "doc": "1109198346", "fecha": "17/12/2005", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Luisa Lopez Meneses", "doc": "1118314328", "fecha": "27/07/2026", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "803", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Grieta en muro y afectación menor.",
        "personas": [
            {"nombre": "Arturo Moreno Ramirez", "doc": "14896625", "fecha": "14/01/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maribel Urrutia", "doc": "31477654", "fecha": "12/02/1975", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "804", "corregimiento": "Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de 1 piso con fisuras leves en mampostería.",
        "personas": [
            {"nombre": "Alba Rosa Pupiales", "doc": "29738375", "fecha": "16/09/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Heladio Pupiales", "doc": "6186899", "fecha": "03/07/1924", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "805", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de 2 pisos con fisuras leves en fachada.",
        "personas": [
            {"nombre": "Henley Ruiz", "doc": "4867045", "fecha": "23/07/1994", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Deynny Chirinos", "doc": "4950136", "fecha": "05/09/1984", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Denley Chirinos", "doc": "4870257", "fecha": "17/09/2005", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Denver Ey Chirinos", "doc": "1872705", "fecha": "29/04/2007", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "806", "corregimiento": "Hacienda Verde", "prioridad": "MEDIA",
        "observaciones_evaluador": "Apto 102 de dos pisos, con placas de carga con fisuras; se sugiere revisión de especialista[cite: 57].",
        "personas": [
            {"nombre": "Humberto Calderon Galindez", "doc": "6135738", "fecha": "28/11/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diana Paola Correa", "doc": "1118299504", "fecha": "12/12/1992", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Julian David Calderon", "doc": "116379080", "fecha": "15/06/2015", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Lauren Calderon", "doc": "1116381285", "fecha": "10/01/2018", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "807", "corregimiento": "El Chocho", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inspección completada con prioridad media[cite: 58].",
        "personas": [
            {"nombre": "Maria Ruth Pino", "doc": "29972503", "fecha": "10/12/1951", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "808", "corregimiento": "Montañitas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con muros apretados y verificación completada[cite: 58].",
        "personas": [
            {"nombre": "Heidy Dasi Muñoz Boting", "doc": "1118302195", "fecha": "23/02/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andres Felipe Ramos", "doc": "1148441786", "fecha": "05/07/1992", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Gua Sebastian Ramos", "doc": "1116378812", "fecha": "08/02/2015", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "809", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble verificado con daños menores[cite: 58].",
        "personas": [
            {"nombre": "Rubilma Barzón Morales", "doc": "29976097", "fecha": "20/12/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hector Elit", "doc": "6341274", "fecha": "22/11/1962", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 782-809...")
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
        print(f"MIGRACIÓN LOTE 782-809 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
