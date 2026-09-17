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
        "num_formulario": "1581", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Valentina Londoño - Sin afectaciones visibles, hacer seguimiento (RUFE-1581).",
        "personas": [{"nombre": "Maria Valentina Londoño", "doc": "1006435412", "fecha": "02/03/2001", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1582", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Elizabeth Gomez Muñoz - Sin afectaciones visibles, realizaron adecuaciones (RUFE-1582).",
        "personas": [{"nombre": "Elizabeth Gomez Muñoz", "doc": "31478223", "fecha": "01/03/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1583", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Zandra Perdomo Gonzalez - Sin afectaciones visibles (RUFE-1583).",
        "personas": [{"nombre": "Zandra Perdomo Gonzalez", "doc": "31477384", "fecha": "01/06/1974", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1584", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Alejandra Montoya Cuenca - Sin afectaciones visibles (RUFE-1584).",
        "personas": [{"nombre": "Maria Alejandra Montoya Cuenca", "doc": "1118283832", "fecha": "06/06/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1585", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Geraldine Delgado Noguera - Sin afectaciones visibles, pendiente adecuaciones fisuras mínimas (RUFE-1585).",
        "personas": [{"nombre": "Geraldine Delgado Noguera", "doc": "171637288", "fecha": "29/08/2000", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1586", "corregimiento": "Fray Peña", "prioridad": "BAJA",
        "observaciones_evaluador": "Maribel Borja Madrid - Vivienda verificada (RUFE-1586).",
        "personas": [{"nombre": "Maribel Borja Madrid", "doc": "31923895", "fecha": "27/08/1961", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1587", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Marta Ahanti Martinez - Prioridad media (RUFE-1587).",
        "personas": [{"nombre": "Marta Ahanti Martinez", "doc": "31478765", "fecha": "29/09/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1588", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jarviu Sagoas Sanabeta / Edua Rocio - Prioridad media (RUFE-1588).",
        "personas": [
            {"nombre": "Jarviu Sagoas", "doc": "16464509", "fecha": "02/07/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Edua Rocio Sanabeta", "doc": "1118287611", "fecha": "04/11/1986", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1589", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Rahiro - Prioridad media (RUFE-1589).",
        "personas": [{"nombre": "Rahiro", "doc": "16645446", "fecha": "15/06/1960", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1581-1589...")
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
        print(f"MIGRACIÓN LOTE 1581-1589 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
