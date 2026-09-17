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
        "num_formulario": "1491", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Restaurante los manzano miravalle dapa - Afectación moderada (RDE-1491).",
        "personas": [{"nombre": "Restaurante Los Manzano", "doc": "1079684038", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1492", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Magic celeste - Afectación baja (RDE-1492).",
        "personas": [{"nombre": "Magic celeste", "doc": "1144040592", "fecha": "01/01/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1493", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "El zar de las arepas - Afectación moderada (RDE-1493).",
        "personas": [{"nombre": "El zar de las arepas", "doc": "16747848", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1494", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Asociación Mundo Mágico de las Sonrisas - Afectación grave (RDE-1494).",
        "personas": [{"nombre": "Asociación Mundo Mágico", "doc": "901369879", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1495", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Silvafriends S.A.S. - Afectación crítica (RDE-1495).",
        "personas": [{"nombre": "Silvafriends S.A.S.", "doc": "901615265", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1496", "corregimiento": "Arroyohondo", "prioridad": "BAJA",
        "observaciones_evaluador": "STM Lock Center S.A. - Sin clasificación (RDE-1496).",
        "personas": [{"nombre": "STM Lock Center S.A.", "doc": "7901474130", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1497", "corregimiento": "Acopi", "prioridad": "ALTA",
        "observaciones_evaluador": "Santana Posada Diana Marcela - Afectación grave (RDE-1497).",
        "personas": [{"nombre": "Diana Marcela Santana Posada", "doc": "1113514759", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1498", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Delgado Vergara Erica Lidalba - Afectación moderada (RDE-1498).",
        "personas": [{"nombre": "Erica Lidalba Delgado Vergara", "doc": "29182436", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1499", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Miscelánea MARY - Sin clasificación (RDE-1499).",
        "personas": [{"nombre": "Miscelánea MARY", "doc": "31583254", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1500", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Empresa Colombiana de Aseo S.A. - Afectación moderada (RDE-1500).",
        "personas": [{"nombre": "Empresa Colombiana de Aseo S.A.", "doc": "805025760", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1501", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Fábrica de Calzado Rómulo S.A.S. - Afectación grave (RDE-1501).",
        "personas": [{"nombre": "Fábrica de Calzado Rómulo S.A.S.", "doc": "800078522", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1502", "corregimiento": "Santa Monica", "prioridad": "BAJA",
        "observaciones_evaluador": "OM Life Comercializadora S.A.S. - Sin clasificación (RDE-1502).",
        "personas": [{"nombre": "OM Life Comercializadora S.A.S.", "doc": "901171677", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1503", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Avendaño Arias Alejandro - Afectación moderada (RDE-1503).",
        "personas": [{"nombre": "Alejandro Avendaño Arias", "doc": "16451790", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1504", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "AG Tex Group S.A.S. - Afectación grave (RDE-1504).",
        "personas": [{"nombre": "AG Tex Group S.A.S.", "doc": "805021170", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1505", "corregimiento": "Cencar", "prioridad": "BAJA",
        "observaciones_evaluador": "Cafetería y Restaurante Rincón Viajero - Sin clasificación (RDE-1505).",
        "personas": [{"nombre": "Cafetería y Restaurante Rincón Viajero", "doc": "87718232", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1506", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Skyline Gastrobar - Sin clasificación (RDE-1506).",
        "personas": [{"nombre": "Skyline Gastrobar", "doc": "164585228", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1491-1506...")
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
        print(f"MIGRACIÓN LOTE 1491-1506 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
