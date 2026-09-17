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
        "num_formulario": "95", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Casa destruida en 85%. Madre cabeza de hogar.",
        "personas": [
            {"nombre": "Dayerly Heredia", "doc": "1007779265", "fecha": "01/02/2000", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alisson Correa", "doc": "1118312645", "fecha": "26/11/2018", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "96", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Paredes, columnas inestables a punto de colapsar. Adulto con discapacidad.",
        "personas": [
            {"nombre": "Luz Mely Esquivel Lopez", "doc": "31475700", "fecha": "01/02/1971", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Snelda Lopez", "doc": "25085730", "fecha": "06/06/1957", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Sneider Heredia", "doc": "16751938", "fecha": "23/11/1968", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Anderson Heredia", "doc": "1006436069", "fecha": "16/03/2003", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "97", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Casa pérdida total, reubicación urgente. De tres pisos con afectaciones en el segundo.",
        "personas": [
            {"nombre": "Francisco Girardi Garcia", "doc": "94446465", "fecha": "24/03/1978", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gloria Diaz", "doc": "29127269", "fecha": "15/01/1980", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Katherin Perez Diaz", "doc": "1151965444", "fecha": "01/06/2002", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Raxella Girardi Diaz", "doc": "1006071555", "fecha": "01/06/2002", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ruth Girardi Diaz", "doc": "1140295398", "fecha": "03/01/2008", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Celeste Girardi Diaz", "doc": "1116385252", "fecha": "25/03/2020", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "98", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Casa en pérdida total, se requiere reubicación. Paredes, columnas inestables a punto de colapsar.",
        "personas": [
            {"nombre": "Paula Andrea Ulloa Espinosa", "doc": "1143838546", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Edinson Lopez", "doc": "16464180", "fecha": "13/03/1984", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "99", "corregimiento": "Miravalle Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda afectada en su totalidad. Paredes en bahareque sin columnas, fracturadas, inestables a punto de colapsar.",
        "personas": [
            {"nombre": "Sabulon Garzon Urbano", "doc": "6342457", "fecha": "08/07/1971", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "100", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Edificación con afectación severa en columnas, vigas, paredes y pisos. Reubicación y ayudas urgente.",
        "personas": [
            {"nombre": "Diana Lorena Moreno", "doc": "1130596367", "fecha": "22/10/1987", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "101", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de tres pisos con afectaciones en el segundo piso 80% afectada en columnas, vigas, paredes.",
        "personas": [
            {"nombre": "German Manbuscay", "doc": "1118299073", "fecha": "30/09/1992", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Olga Elazo", "doc": "31477835", "fecha": "01/01/1980", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Lucio Bolaños", "doc": "94535594", "fecha": "25/03/1974", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Angie Manbuscay", "doc": "1151965060", "fecha": "01/08/1998", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "German Manbuscay", "doc": "16455367", "fecha": "09/07/1973", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Jessica Castaño", "doc": "1118306675", "fecha": "06/06/1996", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "102", "corregimiento": "Miravalle Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Averias en paredes y baño.",
        "personas": [
            {"nombre": "Oliva Savogal Rios", "doc": "29975150", "fecha": "14/04/1954", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Marina Plaza Savogal", "doc": "29975213", "fecha": "03/03/1963", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Hector Humberto Plaza Savogal", "doc": "10483291", "fecha": "02/11/1971", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jhon Jairo Savogal", "doc": "16454446", "fecha": "11/04/1973", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "103", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Averias en paredes, columnas y vigas. Madre cabeza de hogar.",
        "personas": [
            {"nombre": "Saiyuri Elazo", "doc": "1118303286", "fecha": "26/10/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Joaquin Elazo", "doc": "1113313123", "fecha": "02/12/2021", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "104", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Averias en paredes y pisos.",
        "personas": [
            {"nombre": "Maria Alejandra Benavidez", "doc": "1148302737", "fecha": "22/06/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jhonny Cifuentes", "doc": "1006435360", "fecha": "01/01/1990", "es_jefe": False, "sexo": "M", "parentesco": "Esposo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "105", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Averias en paredes, columnas y vigas. Adulto mayor.",
        "personas": [
            {"nombre": "William Heredia", "doc": "6554042", "fecha": "10/05/1957", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "106", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Sistema Estructural agrietado con riesgo de colapso.",
        "personas": [
            {"nombre": "Yadira Bravo Urbano", "doc": "29149983", "fecha": "23/12/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yordi Alexander Gomez", "doc": "1118292322", "fecha": "05/09/1990", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "107", "corregimiento": "Miravalle Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Averias en paredes y baño.",
        "personas": [
            {"nombre": "Andres Felipe Plaza Savogal", "doc": "11306151", "fecha": "01/11/1984", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "108", "corregimiento": "Alto Dapa", "prioridad": "MEDIO",
        "observaciones_evaluador": "Vivienda de dos pisos. Segundo piso prefabricado, canalizacion de aguas.",
        "personas": [
            {"nombre": "Vitalia Verdugo Mazabel", "doc": "31954210", "fecha": "23/11/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "109", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Averias en paredes, pisos y columnas.",
        "personas": [
            {"nombre": "Jorge Cifuentes", "doc": "16448641", "fecha": "12/06/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Ramos", "doc": "31474462", "fecha": "09/04/1987", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Jimmy Bolaños", "doc": "1080900789", "fecha": "17/06/1988", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "110", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Casa prefabricada con afectaciones en techo. Plaquetas separadas.",
        "personas": [
            {"nombre": "Rosa Marina Verdugo", "doc": "31466435", "fecha": "19/04/1955", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Orney Pombo", "doc": "6332201", "fecha": "26/04/1956", "es_jefe": False, "sexo": "M", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Marleny Gaviria V", "doc": "66874824", "fecha": "12/07/1972", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Victor Manuel Gaviria V", "doc": "1105370442", "fecha": "02/05/2007", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "111", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averias en paredes.",
        "personas": [
            {"nombre": "Natalia Acosta", "doc": "1110992065", "fecha": "01/01/2004", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Algenis Realpe", "doc": "31490784", "fecha": "20/05/1976", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "112", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averias en paredes.",
        "personas": [
            {"nombre": "Nolby Amanda Chaguaco", "doc": "29975198", "fecha": "25/02/1958", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maicol Steven Cuervo", "doc": "1109192445", "fecha": "08/02/2011", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "113", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averias en paredes.",
        "personas": [
            {"nombre": "Yineth Lorena Hoyos Osorio", "doc": "1118303412", "fecha": "14/11/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "114", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averias en paredes.",
        "personas": [
            {"nombre": "Isaias Salas", "doc": "1079684038", "fecha": "06/05/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "115", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averias en paredes.",
        "personas": [
            {"nombre": "Patricia Savogal", "doc": "66828005", "fecha": "24/08/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Samuel Rivera S", "doc": "100335806", "fecha": "07/05/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL (Lote 95-115 completo)...")
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
        print(f"MIGRACIÓN FINAL LOTE 95-115 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
