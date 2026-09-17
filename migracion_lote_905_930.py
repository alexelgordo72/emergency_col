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
        "num_formulario": "905", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con afectaciones menores en mampostería no confinada.",
        "personas": [
            {"nombre": "Alvaro H. Torres Correa", "doc": "16459393", "fecha": "28/05/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Melany Torres Velez", "doc": "1007522127", "fecha": "02/06/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Cristean Ortiz", "doc": "1062321639", "fecha": "30/04/1996", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Ximena Velez", "doc": "31483813", "fecha": "07/07/1980", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "906", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda verificada con prioridad media.",
        "personas": [
            {"nombre": "William Harbey Marmolejo C.", "doc": "6548548", "fecha": "19/04/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diana Dilvia Delgado M.", "doc": "1112879874", "fecha": "19/08/1989", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "907", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con fisuras superficiales y verificación completada.",
        "personas": [
            {"nombre": "Erick Morales Galindo", "doc": "16461879", "fecha": "23/11/1998", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Semiletn Mendoza Valencia", "doc": "31480036", "fecha": "06/09/1976", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "908", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con reporte de afectación estructural y verificación completada.",
        "personas": [
            {"nombre": "Jorge Efrain Aguirre Gutierrez", "doc": "6229253", "fecha": "10/07/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Margie Liseth Ceballos Lenis", "doc": "31485993", "fecha": "10/02/1982", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Geraldine", "doc": "1104830929", "fecha": "25/07/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Lourdes Aguirre Ceballos", "doc": "1232802452", "fecha": "01/10/2017", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "909", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble evaluado con prioridad media.",
        "personas": [
            {"nombre": "Cesar Julio Ballesteros Preciado", "doc": "16755880", "fecha": "05/10/1968", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sara Eva Lenis Puente de Ballesteros", "doc": "35534613", "fecha": "07/12/1966", "es_jefe": False, "sexo": "F", "parentesco": "Esposa", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "910", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Apartamento 503A con reporte de daños menores en acabados.",
        "personas": [
            {"nombre": "Emanuel Vincol Chud Leon", "doc": "1118304803", "fecha": "16/07/1995", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria de los Angeles Leon", "doc": "31481821", "fecha": "15/01/1977", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Arcesio Raul Chud", "doc": "1645386", "fecha": "09/07/1968", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "911", "corregimiento": "Uribe Bajo Puente", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble afectado por sismo con grietas en paredes y juntas de columnas; no habitado temporalmente.",
        "personas": [
            {"nombre": "Shon Ariet Murillas Hoyos", "doc": "1118288953", "fecha": "07/07/1988", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ingrid Vanessa Brand Gonzalez", "doc": "1118301397", "fecha": "31/01/1993", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Thiago Murillas Brand", "doc": "1116384810", "fecha": "17/07/2023", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "912", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda afectada por sismo con grietas en paredes y juntas de columnas. No se encuentra habitada, pendiente de evaluación.",
        "personas": [
            {"nombre": "Lina Marcela Gonzalez Realpe", "doc": "1118306502", "fecha": "26/03/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Brayan Eliud Acosta Zuñiga", "doc": "1118304746", "fecha": "03/07/1995", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Salome Acosta Gonzalez", "doc": "1116385157", "fecha": "21/05/2024", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "913", "corregimiento": "Yumbillo", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda rural con inspección completada.",
        "personas": [
            {"nombre": "Luia Nina Muñoz", "doc": "31855787", "fecha": "26/08/1958", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "914", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado en zona urbana.",
        "personas": [
            {"nombre": "Julgo Cedul Castillo V.", "doc": "16462622", "fecha": "04/07/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "915", "corregimiento": "Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con daños menores en mampostería y pintura. Bajo riesgo.",
        "personas": [
            {"nombre": "Pablo Emilio Rodriguez", "doc": "14430294", "fecha": "23/03/1943", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Esperanza Rivadeneira", "doc": "31223408", "fecha": "17/05/1949", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "916", "corregimiento": "Yumbillo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda rural evaluada con prioridad media.",
        "personas": [
            {"nombre": "Hncizar Lopez Ruiz", "doc": "76294944", "fecha": "25/09/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Encida Mayorga Samboni", "doc": "1061985260", "fecha": "09/12/1986", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Miler Johan Lopez Mayorga", "doc": "1110052380", "fecha": "02/04/2013", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "917", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con sistema estructural con mampostería afectada en un 75%. Mediano riesgo.",
        "personas": [
            {"nombre": "Ana Tereza Segura", "doc": "35330314", "fecha": "13/05/1961", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Fernando Cabrera", "doc": "14967812", "fecha": "14/09/1950", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "918", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda colapsada, Riesgo Alto. Planillada para casa prefabricada.",
        "personas": [
            {"nombre": "Hernan Alberto Ortiz Muñoz", "doc": "16445009", "fecha": "04/08/1954", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Martha Lucia Ortiz Benavidez", "doc": "1144075791", "fecha": "05/12/1994", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Blanca Graciela Benavidez Urbano", "doc": "29975259", "fecha": "29/11/1960", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Wisner Artey Martinez Males", "doc": "1118296830", "fecha": "17/09/1991", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Daniel Ortiz Benavidez", "doc": "1118293823", "fecha": "18/05/1991", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Drious Martinez Ortiz", "doc": "1104842541", "fecha": "10/03/2018", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "919", "corregimiento": "Yumbillo", "prioridad": "ALTA",
        "observaciones_evaluador": "Inmueble rural con evaluación completada.",
        "personas": [
            {"nombre": "Tidal Paulina", "doc": "6554009", "fecha": "12/03/1948", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cerom", "doc": "29984063", "fecha": "13/03/1945", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "920", "corregimiento": "Yumbillo", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con fisuras verticales y desplome de muros divisorios internos y externos.",
        "personas": [
            {"nombre": "Conovalo Lopez", "doc": "29984073", "fecha": "13/09/1955", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Falisa Ramos Lopez", "doc": "1118295860", "fecha": "09/03/1991", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Miguel Angel Ramos Lopez", "doc": "1118295946", "fecha": "09/09/1987", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ratac Ramos Lopez", "doc": "0", "fecha": "05/09/2009", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "921", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con hectáreas verificadas y mampostería evaluada.",
        "personas": [
            {"nombre": "Hidelver Devavides Muñoz", "doc": "6343478", "fecha": "05/08/1993", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alba Lia Muñoz Saplyer", "doc": "48610502", "fecha": "15/10/1961", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Jhou Edinson Capote Muñoz", "doc": "1116376052", "fecha": "03/07/2011", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Yuvani Muñoz Sapuyer", "doc": "1118300400", "fecha": "08/05/1993", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "922", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble rural verificado.",
        "personas": [
            {"nombre": "Delandu Galindo", "doc": "1932729", "fecha": "25/02/1957", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "923", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Finca rural con reporte de afectaciones en terreno y cultivos de café.",
        "personas": [
            {"nombre": "Ramiro Lopera", "doc": "14945190", "fecha": "24/05/1946", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Lidia Prado Quiñon", "doc": "31209540", "fecha": "03/08/1948", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Martha Clemencia Martinez Giraldo", "doc": "29931010", "fecha": "10/01/1972", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "924", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con evaluación completada.",
        "personas": [
            {"nombre": "Juan Francisco Blanco", "doc": "16592259", "fecha": "16/06/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Mia Del Consuelo Saillon Garcia", "doc": "31296950", "fecha": "01/01/1953", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "925", "corregimiento": "La Olga", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda rural con grietas en paredes y daños en tubería de agua.",
        "personas": [
            {"nombre": "Alirio Bahos Logros", "doc": "4622331", "fecha": "09/01/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "926", "corregimiento": "La Olga", "prioridad": "MEDIA",
        "observaciones_evaluador": "Afectación en marquesina de secado de café y grietas en soportes de placa.",
        "personas": [
            {"nombre": "Luis Carlos Hogas Mariño", "doc": "14966103", "fecha": "11/10/1949", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Doris", "doc": "31982960", "fecha": "05/02/1955", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "927", "corregimiento": "La Olga", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda rural con pisos agrietados y derrumbe de terreno en bahareque.",
        "personas": [
            {"nombre": "Antonio Hoyos Muñoz", "doc": "14840010", "fecha": "14/07/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "928", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en pisos y paredes, daño en marquesina y fosa de la pulpa de café.",
        "personas": [
            {"nombre": "Heberth Riascos Urbano", "doc": "14974735", "fecha": "07/08/1951", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Daicy Viveros Martinez", "doc": "31253233", "fecha": "02/09/1953", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "929", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grietas en paredes, cielo raso y pisos de la vivienda y bodega.",
        "personas": [
            {"nombre": "Liliana Patricia Gutierrez Tamayo", "doc": "31573826", "fecha": "08/08/1979", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "930", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Paredes de las habitaciones con riesgo de caída, fisuradas y daños en cielo raso.",
        "personas": [
            {"nombre": "Julio Cesar Ospina Reyes", "doc": "16777586", "fecha": "13/01/1969", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Losana Ospina Reyes", "doc": "31952529", "fecha": "05/04/1937", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "José Antonio Ospina Reyes", "doc": "16751012", "fecha": "28/11/1966", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 905-930...")
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
        print(f"MIGRACIÓN LOTE 905-930 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
