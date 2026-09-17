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
        "num_formulario": "83", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fractura en paredes, desprendimiento de losa en el frente, caída de techo y cielo de la parte delantera.",
        "personas": [
            {"nombre": "Leidy Montes", "doc": "29398080", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "84", "corregimiento": "Bolivar", "prioridad": "BAJA",
        "observaciones_evaluador": "Desprendimiento de cubierta, barda perimetral de la terraza suelta con riesgo inminente de caída a predios vecinos.",
        "personas": [
            {"nombre": "Margarita Fernandez", "doc": "29940795", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "85", "corregimiento": "Bolivar", "prioridad": "BAJA",
        "observaciones_evaluador": "Daños en muros no estructurales y escaleras, con posible desprendimiento del muro que colinda con el baño.",
        "personas": [
            {"nombre": "Julio Cesar Apolindar Sanchez", "doc": "16446337", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "86", "corregimiento": "Pizarro", "prioridad": "BAJA",
        "observaciones_evaluador": "Muros divisorios fracturados en el segundo piso, muy comprometidos, algunos deben demolerse.",
        "personas": [
            {"nombre": "Maria Ludibia Osorio Murillo", "doc": "1118283542", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "87", "corregimiento": "Guadalupe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Movimiento de estructura y afectación en segundo piso con desprendimiento de ladrillos en ventana por falta de confinamiento.",
        "personas": [
            {"nombre": "Mariela Benavides", "doc": "25714867", "fecha": "01/01/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "88", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Institución sin ánimo de lucro (Casín) con daños en muros no estructurales en la zona media del edificio.",
        "personas": [
            {"nombre": "Ruth Ximena Satizabal Garcia", "doc": "1118286076", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "89", "corregimiento": "Las Vegas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque con colapso de elementos y recomendación de urgente reubicación.",
        "personas": [
            {"nombre": "Alberto Suarez", "doc": "4538717", "fecha": "01/01/1960", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "90", "corregimiento": "La Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Construcción en estructura deficiente; recomendación urgente de desocupar y demoler por afectar a vecinos.",
        "personas": [
            {"nombre": "Rafael Jandido Ruiz", "doc": "17041291", "fecha": "01/01/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "91", "corregimiento": "La Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda unifamiliar prefabricada expuesta por la construcción vecina construida con elementos oxidados.",
        "personas": [
            {"nombre": "Sandra Jimenez Loaiza", "doc": "31476834", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "92", "corregimiento": "Finlandia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Afectaciones en fachada principal del cuarto piso.",
        "personas": [
            {"nombre": "Diana Marcela Duque", "doc": "1038413096", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "94", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muro de mampostería sin apoyo y mal elaborado en el interior.",
        "personas": [
            {"nombre": "Lady Alba Daza", "doc": "31471424", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 83-94...")
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
        print(f"MIGRACIÓN LOTE 83-94 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
