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
    },
    {
        "num_formulario": "148", "corregimiento": "Nueva Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Daños en estructura de vigas y columnas expuestas. Escaleras de la losa prácticamente colapsadas.",
        "personas": [
            {"nombre": "Christian Cardona", "doc": "1041610477", "fecha": "01/01/1987", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Leonor Garcia", "doc": "0", "fecha": "01/01/1982", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Laura Garcia", "doc": "0", "fecha": "01/01/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Daniel Garcia", "doc": "0", "fecha": "01/01/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ubaldina Martinez", "doc": "0", "fecha": "01/01/1954", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "149", "corregimiento": "Miravalle Norte", "prioridad": "ALTA",
        "observaciones_evaluador": "Afectaciones estructurales o funcionales parciales. Hogar con persona con discapacidad (retraso mental moderado).",
        "personas": [
            {"nombre": "Silvia Costanza Castillo", "doc": "29940982", "fecha": "01/01/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Michael Caicedo", "doc": "0", "fecha": "01/01/2008", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ofir Celle Velez", "doc": "0", "fecha": "01/01/1959", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "150", "corregimiento": "La Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque colapsada en partes, cielo rasos colapsados y paredes afectadas. Diagnóstico de salud crítico (cáncer de garganta en integrante).",
        "personas": [
            {"nombre": "Doris del Socorro Cardona", "doc": "42771852", "fecha": "01/01/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Edinson Restrepo Cardona", "doc": "1163995", "fecha": "01/01/1998", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Angui Sofia Cardona", "doc": "0", "fecha": "01/01/2011", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Maximiliano Cardona", "doc": "0", "fecha": "01/01/2013", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "151", "corregimiento": "Panorama", "prioridad": "ALTA",
        "observaciones_evaluador": "Fisuras en columnas y vigas de cimentación, escalera suelta hacia el patio, asentamiento en parte trasera.",
        "personas": [
            {"nombre": "Luis Horacio Gil Valencia", "doc": "14970066", "fecha": "06/12/1950", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "152", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Movimiento en paredes por falta de columnas. Se han apuntalado áreas de la casa.",
        "personas": [
            {"nombre": "Jhon Fonseca", "doc": "16463029", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "153", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Desprendimiento de 4 muros no estructurales en ambos pisos a raíz del sismo.",
        "personas": [
            {"nombre": "Ana Milena Lerma", "doc": "31488552", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "154", "corregimiento": "Juan Pablo II", "prioridad": "MEDIA",
        "observaciones_evaluador": "Afectaciones por errores constructivos, mampostería sin confinamiento, falta de anclaje y falla en la pega (2do y 3er piso).",
        "personas": [
            {"nombre": "Liliana Manzano Betancourt", "doc": "31471943", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 145-154...")
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
        print(f"MIGRACIÓN LOTE 145-154 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
