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
        "num_formulario": "221",
        "corregimiento": "Dapa",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Estructura Comprometida, columnas y losa de entrepiso, techos colapsados.",
        "personas": [
            {"nombre": "Claudia Rocio Giraldo Riaño", "doc": "41916224", "fecha": "01/03/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jaime Orlando Poveda Forero", "doc": "7556973", "fecha": "10/09/1968", "es_jefe": False, "sexo": "M", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Jhonny Alejandro Poveda Giraldo", "doc": "1151957996", "fecha": "24/04/1995", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "231",
        "corregimiento": "La Buitrera",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda colapsada en su sistema estructural, mampostería y red eléctrica.",
        "personas": [
            {"nombre": "Rocket Artemio Ortiz", "doc": "76221393", "fecha": "01/10/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Marina Perafan", "doc": "34547585", "fecha": "19/11/1966", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Rocket Ancisar Ortiz Perafan", "doc": "1006253064", "fecha": "01/09/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Danny Julieth Ortiz Perafan", "doc": "1114735943", "fecha": "16/11/1997", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Edward Alexander Ortiz Perafan", "doc": "1118305429", "fecha": "28/10/1995", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "226",
        "corregimiento": "El Pedregal",
        "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque colapsada, sin sistema de estructura.",
        "personas": [
            {"nombre": "Juan Carlos Salazar Castaño", "doc": "16750200", "fecha": "01/08/1967", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Febe Benitez Rubiano", "doc": "51724716", "fecha": "24/04/1963", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"}
        ]
    }
]

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match:
        return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO (Upsert) de datos en tablas originales...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        formularios_creados = 0
        formularios_actualizados = 0
        personas_creadas = 0
        personas_actualizadas = 0
        
        for form in LOTES_NUEVOS_RUFE:
            num_limpio = form["num_formulario"].lstrip('0')
            
            # --- LÓGICA DE FORMULARIO ---
            cur.execute("SELECT id FROM public.rufe_formularios WHERE numero_formulario = %s", (num_limpio,))
            resultado = cur.fetchone()
            
            if resultado:
                form_id = resultado[0]
                cur.execute("""
                    UPDATE public.rufe_formularios 
                    SET prioridad = %s, observaciones_evaluador = %s
                    WHERE id = %s;
                """, (form["prioridad"], form["observaciones_evaluador"], form_id))
                formularios_actualizados += 1
            else:
                cur.execute("""
                    INSERT INTO public.rufe_formularios 
                    (reporte_id, numero_formulario, corregimiento, prioridad, observaciones_evaluador)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (str(uuid.uuid4()), num_limpio, form["corregimiento"], form["prioridad"], form["observaciones_evaluador"]))
                form_id = cur.fetchone()[0]
                formularios_creados += 1
                
            # --- LÓGICA DE PERSONAS ---
            for p in form["personas"]:
                edad_calc = calcular_edad_2026(p["fecha"])
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE REPLACE(documento_identidad, '.', '') = %s", (p["doc"],))
                res_persona = cur.fetchone()
                
                if res_persona:
                    persona_id = res_persona[0]
                    cur.execute("""
                        UPDATE public.rufe_personas 
                        SET fecha_nacimiento = %s, edad = %s, es_jefe_hogar = %s, parentesco = %s, sexo = %s, etnia = %s
                        WHERE id = %s;
                    """, (p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], persona_id))
                    personas_actualizadas += 1
                else:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, edad, es_jefe_hogar, parentesco, sexo, etnia, activo)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, true)
                    """, (form_id, p["nombre"], p["doc"], p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"]))
                    personas_creadas += 1

        print(f"\n==================================================")
        print(f"MIGRACIÓN Y ENRIQUECIMIENTO EXITOSO.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
