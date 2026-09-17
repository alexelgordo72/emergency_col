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
        "num_formulario": "1112", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Calzado Dos 21 - Establecimiento comercial verificado sin observaciones críticas (RDE-1112)[cite: 74].",
        "personas": [{"nombre": "Calzado Dos 21", "doc": "1118292415", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1172", "corregimiento": "Guacandá", "prioridad": "MEDIA",
        "observaciones_evaluador": "Dan Metro - Microempresa industrial operando parcialmente (RDE-1172)[cite: 74].",
        "personas": [{"nombre": "Dan Metro", "doc": "1118295197", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1173", "corregimiento": "Madrigal", "prioridad": "BAJA",
        "observaciones_evaluador": "Kuki Pan Madrigal - Panadería funcionando con normalidad y atención al público (RDE-1173).",
        "personas": [{"nombre": "Kuki Pan Madrigal", "doc": "118284992", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1174", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Divina Variedad - Comercio con daños leves en mercancía, esmaltes rotos y lámparas (RDE-1174).",
        "personas": [{"nombre": "Divina Variedad", "doc": "1118310384", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1175", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Casino Central Park Bolívar - Local operando con normalidad sin afectaciones (RDE-1175).",
        "personas": [{"nombre": "Casino Central Park Bolívar", "doc": "1118311317", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1176", "corregimiento": "Buenos Aires", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vidrios y Aluminios Rodríguez - Daños en infraestructura física y herramientas de trabajo (RDE-1176).",
        "personas": [{"nombre": "Vidrios y Aluminios Rodríguez", "doc": "1110591176", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1177", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Depósito de Alimentos Parre - Establecimiento verificado sin novedades (RDE-1177).",
        "personas": [{"nombre": "Depósito de Alimentos Parre", "doc": "6098662", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1178", "corregimiento": "Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Hospedaje - Establecimiento con daños estimados en 30 millones y recuperación en 30 días (RDE-1178).",
        "personas": [{"nombre": "Hospedaje", "doc": "16454723", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1179", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "FEDY - Establecimiento con instalaciones en buen estado (RDE-1179).",
        "personas": [{"nombre": "FEDY", "doc": "1118311177", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1180", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Auto Garcia - Taller automotriz sin afectaciones de ningún tipo (RDE-1180).",
        "personas": [{"nombre": "Auto Garcia", "doc": "16458159", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1111-1170...")
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
        print(f"MIGRACIÓN LOTE 1111-1170 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
