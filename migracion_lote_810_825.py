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
        "num_formulario": "810", "corregimiento": "Belalcazar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con riesgo medio de afectación en acabados y mampostería.",
        "personas": [
            {"nombre": "Maria Yolanda Caredo Acosta", "doc": "299722", "fecha": "30/06/1950", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Marigna", "doc": "1027807866", "fecha": "27/02/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Catalina Silva Montero", "doc": "31487489", "fecha": "28/04/1979", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "811", "corregimiento": "Finlandia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras en muros y elementos no estructurales.",
        "personas": [
            {"nombre": "Tez Getia", "doc": "6463299", "fecha": "28/04/1963", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Arturo", "doc": "1144524368", "fecha": "14/03/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Alejandro Sandoval Velaro", "doc": "34672295", "fecha": "17/07/1973", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "812", "corregimiento": "Belalcazar", "prioridad": "ALTA",
        "observaciones_evaluador": "Casa en bahareque con múltiples grietas y alto riesgo estructural.",
        "personas": [
            {"nombre": "Hector Fabio Bejarano Quintero", "doc": "16445551", "fecha": "11/02/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Agripina Bejarano Quintero", "doc": "31470011", "fecha": "15/03/1966", "es_jefe": False, "sexo": "F", "parentesco": "Hermano(a)", "etnia": "Ninguna"},
            {"nombre": "Nubia Marina Bejarano Quintero", "doc": "31465785", "fecha": "01/01/1968", "es_jefe": False, "sexo": "F", "parentesco": "Hermano(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Sebastian Bejarano Bonero", "doc": "118307045", "fecha": "20/06/2007", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Danna Gzeth Bejarano Bonero", "doc": "118311431", "fecha": "10/07/1982", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Agustin Alban Bejarano", "doc": "1116378975", "fecha": "28/03/2018", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "813", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con adecuaciones pertinentes ya realizadas.",
        "personas": [
            {"nombre": "Elizabeth Villamil Ibarra", "doc": "1116733633", "fecha": "07/01/1998", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alfonso Villamil Ibarra", "doc": "1118259176", "fecha": "31/07/1994", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Santiago Ouro Villamil", "doc": "1116733206", "fecha": "10/06/2015", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "814", "corregimiento": "Finlandia", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales leves en acabados y mampostería. Habitable.",
        "personas": [
            {"nombre": "Vidiolclaya Mera Serna", "doc": "1144187870", "fecha": "14/07/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Fabian Andres Serna", "doc": "1118283248", "fecha": "22/05/1986", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "815", "corregimiento": "Guadubas / Comfandi", "prioridad": "ALTA",
        "observaciones_evaluador": "Apto 605, baldosa de la sala fracturada, paneles de cielo raso desprendidos, desprendimiento de pañete y grietas que atraviesan los muros[cite: 60].",
        "personas": [
            {"nombre": "Moira Alucliet Martinez", "doc": "1143949195", "fecha": "16/04/1992", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Robinson David Falla", "doc": "1144156723", "fecha": "16/04/1992", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "816", "corregimiento": "Comfandi", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras transversales (superficiales), fisuras en el baño por separación de elementos, desprendimiento de cielo raso y grietas horizontales entre muro y viga.",
        "personas": [
            {"nombre": "Lilibeth Villalobos Yepes", "doc": "39578797", "fecha": "20/06/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Samuel Arias Naranjo", "doc": "1144212533", "fecha": "05/10/1990", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Heidy Yulieth Naranjo Villalobos", "doc": "1144212533", "fecha": "23/12/1984", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "John Yolanda Martinez", "doc": "16938126", "fecha": "01/01/1975", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "817", "corregimiento": "Fray Peña", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado con revisión estructural completada.",
        "personas": [
            {"nombre": "Dominguez", "doc": "0", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "818", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con daños en las estructuras; existe riesgo, se recomienda seguimiento[cite: 61].",
        "personas": [
            {"nombre": "Maria Natividad Rosales", "doc": "66836476", "fecha": "25/05/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "819", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Daños en muros y techos por desprendimiento.",
        "personas": [
            {"nombre": "Maria Emma Perez Galindo", "doc": "29581636", "fecha": "01/04/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Victor Julio Peña Ramos", "doc": "94281818", "fecha": "11/06/1972", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "820", "corregimiento": "Bellavista", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado sin riesgo, con fisuras superficiales[cite: 62].",
        "personas": [
            {"nombre": "Nora Solarte Tovar", "doc": "31467346", "fecha": "05/02/1959", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "821", "corregimiento": "Trinidad", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muros y pisos con grietas, filtraciones y desprendimiento de repellos[cite: 62].",
        "personas": [
            {"nombre": "Martha Lucia Monus Velasco", "doc": "31466947", "fecha": "11/01/1956", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Freddy Edinson Campo", "doc": "16769534", "fecha": "01/01/1970", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "822", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Manchones en losa, separación de aliviadero en muro y columna con fisuras[cite: 62].",
        "personas": [
            {"nombre": "Flor Alba Quiguapungo", "doc": "34598972", "fecha": "01/01/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "823", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en habitación principal sobre pared y cielo raso, fisuras en la losa superior[cite: 63].",
        "personas": [
            {"nombre": "Diona Soto Lopez", "doc": "11441541709", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Julian Cotono Lopez", "doc": "6113695657", "fecha": "01/01/1995", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "824", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda revisada con reporte de estabilidad general.",
        "personas": [
            {"nombre": "Sandro Eugenia Zamora", "doc": "31978022", "fecha": "04/08/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "825", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado con prioridad baja[cite: 63].",
        "personas": [
            {"nombre": "Asnoraldo Mendoza", "doc": "314350709", "fecha": "16/07/1948", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Adriana Mendoza", "doc": "1232795405", "fecha": "25/11/1983", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Salome", "doc": "0", "fecha": "23/12/2015", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Alba Ines Ossa de Mendoza", "doc": "29972739", "fecha": "16/07/1952", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 810-825...")
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
        print(f"MIGRACIÓN LOTE 810-825 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
