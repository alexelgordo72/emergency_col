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
        "num_formulario": "1554", "corregimiento": "Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Gelexonder Medina - Vivienda de 1 piso con fisuras en muros traseros, se recomienda reforzamiento (RUFE-1554)[cite: 54].",
        "personas": [
            {"nombre": "Gelexonder Medina", "doc": "79644285", "fecha": "20/03/1973", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Zenericth Parra Morales", "doc": "5276114", "fecha": "07/08/1973", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1555", "corregimiento": "Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Sebastian Villa Sanchez - Fisuras leves, riesgo por desnivel con vivienda vecina más alta (RUFE-1555)[cite: 54].",
        "personas": [
            {"nombre": "Sebastian Villa Sanchez", "doc": "1118307428", "fecha": "14/11/1996", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Natalia Andrea Sanchez Villa", "doc": "1005911164", "fecha": "01/01/2002", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1556", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Yuliana Ramos Guerrero - Fisuras sin mampostería afectada, se recomienda reparar y colocar anclajes (RUFE-1556)[cite: 55].",
        "personas": [
            {"nombre": "Yuliana Ramos Guerrero", "doc": "7394459185", "fecha": "01/01/1999", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juan Diego Guerrero", "doc": "7709189145", "fecha": "25/07/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1557", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Angel Alberto Mendoza - Ampliación trasera (cocina) con necesidad de refuerzo en muros (RUFE-1557)[cite: 55].",
        "personas": [
            {"nombre": "Angel Alberto Mendoza", "doc": "16446014", "fecha": "25/06/1956", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Rosario Rubiera", "doc": "31919220", "fecha": "13/05/1965", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1558", "corregimiento": "Estancia Vieja", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jaime Neura Alarade - Vivienda de 2 pisos de interés social con muros agrietados, se recomienda evaluación (RUFE-1558)[cite: 56].",
        "personas": [
            {"nombre": "Jaime Neura Alarade", "doc": "1118283573", "fecha": "08/07/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jaime Neura Mane", "doc": "16448897", "fecha": "23/09/1960", "es_jefe": False, "sexo": "M", "parentesco": "Padre/Madre", "etnia": "Ninguna"},
            {"nombre": "Gloria Estela Alarade", "doc": "29739112", "fecha": "16/10/1960", "es_jefe": False, "sexo": "F", "parentesco": "Padre/Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1559", "corregimiento": "Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jhonn Elicio Calpa Sanchez - Vivienda de 2 pisos, placa afectada por columna negativa, se recomienda terminar confinamiento (RUFE-1559)[cite: 56].",
        "personas": [
            {"nombre": "Jhonn Elicio Calpa Sanchez", "doc": "7062775279", "fecha": "15/09/1937", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jhon Elicio Calpa Sanchez", "doc": "7062776719", "fecha": "02/07/2009", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1560", "corregimiento": "La Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Lucelly Cordoba - Vivienda de 1 piso con fisuras en muros, se recomienda reforzamiento (RUFE-1560)[cite: 56].",
        "personas": [
            {"nombre": "Lucelly Cordoba", "doc": "40363084", "fecha": "30/09/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ene Noguera Cordoba", "doc": "1086222071", "fecha": "03/05/1986", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1561", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jakeline Alzate Quintero - Vivienda de 2 pisos con fisuras en muros al 1er nivel (RUFE-1561)[cite: 55].",
        "personas": [
            {"nombre": "Jakeline Alzate Quintero", "doc": "1112101277", "fecha": "30/01/2000", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1562", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jose Alberto Gutierrez Blandon - Vivienda de 2 pisos con muros agrietados, se recomienda evaluación (RUFE-1562)[cite: 53].",
        "personas": [
            {"nombre": "Jose Alberto Gutierrez Blandon", "doc": "1118825165", "fecha": "07/03/1991", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yekeline Calcedo", "doc": "7073323981", "fecha": "23/09/1972", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1563", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Misael Cardenas - Vivienda con fisuras y desprendimiento de mampostería en losa y sala (RUFE-1563)[cite: 52].",
        "personas": [
            {"nombre": "Misael Cardenas", "doc": "6247850", "fecha": "14/07/1967", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gloria Escobar", "doc": "29942112", "fecha": "14/01/1972", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1554-1563...")
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
        print(f"MIGRACIÓN LOTE 1554-1563 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
