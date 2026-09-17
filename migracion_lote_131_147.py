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
        "num_formulario": "131", "corregimiento": "Manga Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras de mampostería en juntas con columnas y caída de balcón en segundo piso. Habitable.",
        "personas": [
            {"nombre": "Rolando Ibarra", "doc": "94361041", "fecha": "30/07/1973", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Estella Castillo Acevedo", "doc": "31476424", "fecha": "29/09/1973", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Juan Stevan Castillo Giraldo", "doc": "1119278503", "fecha": "23/10/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jhaaisa Gonzales", "doc": "30982012", "fecha": "28/01/2002", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Evangelin Castillo Gonzales", "doc": "1116385025", "fecha": "14/01/2024", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "132", "corregimiento": "Manga Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Incendio Manga Vieja. Vivienda consumida en su totalidad por incendio, pérdida total.",
        "personas": [
            {"nombre": "Edinson Caveras", "doc": "16672024", "fecha": "10/07/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Alvilia Sinuaquiva", "doc": "31890979", "fecha": "13/03/1962", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "133", "corregimiento": "Alto Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda construida en bahareque, con fisuras en juntas de los muros y desprendimiento de material. Completamente habitable.",
        "personas": [
            {"nombre": "Vitalia Garcia", "doc": "29939597", "fecha": "04/11/1956", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Lizandro Ibarra", "doc": "16462291", "fecha": "01/09/1980", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Diana Marcela Martinez Ibarra", "doc": "1087645655", "fecha": "19/03/1992", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Mauricio Ibarra", "doc": "94361862", "fecha": "01/01/1979", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Andres Felipe Agudelo Ibarra", "doc": "1116372981", "fecha": "01/01/2006", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "134", "corregimiento": "Manga Vieja", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material, con múltiples grietas y cubierto parcialmente colapsado, con elementos estructurales ausentes.",
        "personas": [
            {"nombre": "Flower Martinez Quintero", "doc": "16450967", "fecha": "09/03/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Piedad Zapata Martinez", "doc": "291940224", "fecha": "04/08/1970", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Misael Martinez", "doc": "16453290", "fecha": "07/08/1970", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "135", "corregimiento": "Manga Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras en juntas de muro y desprendimiento de recubrimiento en mampostería y vigas. Es habitable.",
        "personas": [
            {"nombre": "Numa Pompilio Castillo Ibarra", "doc": "6531294", "fecha": "01/10/1966", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Esperanza Quitombo", "doc": "1118286858", "fecha": "10/06/1987", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Gisell Aguila Quitumbo", "doc": "11183139", "fecha": "16/02/2005", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "136", "corregimiento": "Manga Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con afectaciones leves, fisuras en mampostería de muros divisorios. Completamente habitable.",
        "personas": [
            {"nombre": "Maria Ximena Vergara Vergara", "doc": "31487153", "fecha": "15/10/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Paula Melo Vergara", "doc": "1116376696", "fecha": "11/04/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "137", "corregimiento": "Manga Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en material con columnas construidas solo con ladrillos fracturados sin acero estructural. Cubierta parcialmente colapsada. No habitable.",
        "personas": [
            {"nombre": "Lilia Maria Oviedo Perez", "doc": "31475688", "fecha": "25/05/1971", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Estefania Martinez Oviedo", "doc": "1116376058", "fecha": "22/06/2011", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Nataly Vivas Blandon", "doc": "1116378009", "fecha": "24/12/2013", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Yary Katherine Blandon", "doc": "1007779367", "fecha": "18/04/2000", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jorge Armando Oviedo Perez", "doc": "1118301926", "fecha": "18/04/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Alana Valhalla", "doc": "1116383519", "fecha": "24/01/2021", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "138", "corregimiento": "Manga Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de dos plantas. Separaciones y fisuras en juntas entre columnas y en muros divisorios. Habitable.",
        "personas": [
            {"nombre": "Maria Elena Oviedo Jasso", "doc": "29980205", "fecha": "20/07/1957", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luis Miguel Corrales Lasso", "doc": "1116372208", "fecha": "03/06/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Daniela Lasso Corrales", "doc": "1113624166", "fecha": "10/01/2002", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Alan Matias Lasso Corrales", "doc": "1239688775", "fecha": "25/05/2022", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "139", "corregimiento": "Manga Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en material, con sus muros internos sueltos, vigas y columnas no presentan fallas pero mampostería comprometida. Riesgo de colapso. No habitable.",
        "personas": [
            {"nombre": "Isidoro Vergara", "doc": "16448988", "fecha": "26/01/1961", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Yuly Vergara Trujillo", "doc": "1118286929", "fecha": "14/08/2005", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jhon Brandon Vergara Trujillo", "doc": "1111544793", "fecha": "30/11/2006", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Alex Juan Pol Vergara Trujillo", "doc": "1109566543", "fecha": "06/11/2018", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "140", "corregimiento": "Manga Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de bahareque con sus muros colapsados y soportes debilitados. Riesgo latente. No habitar.",
        "personas": [
            {"nombre": "Sonia Patricia Oviedo Jasso", "doc": "31475959", "fecha": "18/12/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jose Ney Garcia Gonzales", "doc": "76306134", "fecha": "05/10/1967", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "141", "corregimiento": "Manga Vieja", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda construida en material, con fisuras en muros divisorios, desplomes en juntas y cuchilla.",
        "personas": [
            {"nombre": "Jose Isaias Jasso Ramos", "doc": "6552125", "fecha": "22/05/1958", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Eugenia Jasso", "doc": "2998020", "fecha": "04/06/1961", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "142", "corregimiento": "Panorama", "prioridad": "ALTA",
        "observaciones_evaluador": "Afectaciones menores en cielo raso, fisuras en paredes de baño y pequeña fisura en viga.",
        "personas": [
            {"nombre": "Luis Horacio Gil Valencia", "doc": "14970066", "fecha": "06/12/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Rosmira Durango", "doc": "25052722", "fecha": "17/11/1946", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "143", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Sin novedad relevante.",
        "personas": [
            {"nombre": "Margarita Viafara", "doc": "31915601", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "144", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Daños en paredes no estructurales, supervisar fisuras.",
        "personas": [
            {"nombre": "Denny Muñoz Campo", "doc": "166988617", "fecha": "20/01/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "145", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda habitable, segura.",
        "personas": [
            {"nombre": "Cenaido Muñoz", "doc": "29939548", "fecha": "01/01/1960", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "146", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en paredes, requiere reparación de dintel de baño.",
        "personas": [
            {"nombre": "Yorlady Villegas Gomez", "doc": "1118288625", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "147", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Necesita silla de ruedas. Atención social requerida.",
        "personas": [
            {"nombre": "Jose Luis Loaiza Escobar", "doc": "2776217", "fecha": "01/01/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 131-147...")
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
        print(f"MIGRACIÓN LOTE 131-147 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
