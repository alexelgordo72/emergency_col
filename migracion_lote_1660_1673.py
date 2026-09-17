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
        "num_formulario": "1660", "corregimiento": "Yunorama Alto", "prioridad": "BAJA",
        "observaciones_evaluador": "Laura Isabel Mejia Garciro - Prioridad baja, habitable (RUFE-1660)[cite: 41].",
        "personas": [
            {"nombre": "Laura Isabel Mejia Garciro", "doc": "1005744140", "fecha": "30/05/2000", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1661", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Puri Marcela Guaspero Guadial - Prioridad baja (RUFE-1661)[cite: 41].",
        "personas": [
            {"nombre": "Puri Marcela Guaspero Guadial", "doc": "31307765", "fecha": "01/01/1983", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1662", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Julia Rosa Jaramillo Vallejo - Prioridad baja (RUFE-1662)[cite: 41].",
        "personas": [
            {"nombre": "Julia Rosa Jaramillo Vallejo", "doc": "31469026", "fecha": "19/03/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Edier Antonio Paladines", "doc": "16446553", "fecha": "05/08/1955", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1663", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Stela Lopez Preciado - Bloques de roca sueltos pequeños en vivienda, se recomienda seguimiento (RUFE-1663)[cite: 41].",
        "personas": [
            {"nombre": "Stela Lopez Preciado", "doc": "31481887", "fecha": "22/09/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1664", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria del Rosario Pinchao Vergara - Cariñositos 2, prioridad baja (RUFE-1664)[cite: 41].",
        "personas": [
            {"nombre": "Maria del Rosario Pinchao Vergara", "doc": "66933960", "fecha": "25/08/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1665", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Hardy Xiomara Zapata Parra - Placique Jacinto, prioridad baja (RUFE-1665)[cite: 41].",
        "personas": [
            {"nombre": "Hardy Xiomara Zapata Parra", "doc": "1118285375", "fecha": "27/04/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1666", "corregimiento": "Pizarro", "prioridad": "BAJA",
        "observaciones_evaluador": "Katerine Valbuana - Los Pingüinos, prioridad baja (RUFE-1666)[cite: 41].",
        "personas": [
            {"nombre": "Katerine Valbuana", "doc": "1130594277", "fecha": "28/06/1987", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1667", "corregimiento": "Las Américas", "prioridad": "BAJA",
        "observaciones_evaluador": "Gladiz Rojas Fonta - Las Estrellitas, prioridad baja (RUFE-1667)[cite: 41].",
        "personas": [
            {"nombre": "Gladiz Rojas Fonta", "doc": "1118302964", "fecha": "24/08/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1668", "corregimiento": "Las Américas", "prioridad": "BAJA",
        "observaciones_evaluador": "Jonny Lorena Alegria Beltran - Mis Primeros Años, prioridad baja (RUFE-1668)[cite: 41].",
        "personas": [
            {"nombre": "Jonny Lorena Alegria Beltran", "doc": "1118306153", "fecha": "09/03/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1669", "corregimiento": "San Jorge", "prioridad": "BAJA",
        "observaciones_evaluador": "Oliva de Jesus Taborda Toro - Mis Pequeños Picarines, prioridad baja (RUFE-1669)[cite: 41].",
        "personas": [
            {"nombre": "Oliva de Jesus Taborda Toro", "doc": "43475630", "fecha": "22/03/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1670", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Diana Jimena Agredo Quetio - Prioridad baja (RUFE-1670)[cite: 41].",
        "personas": [
            {"nombre": "Diana Jimena Agredo Quetio", "doc": "1118260199", "fecha": "26/10/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jaz Alejandro Ramos Agredo", "doc": "1104841220", "fecha": "17/07/2017", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1671", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Leida Bedoya - Ya habían realizado reparaciones (RUFE-1671)[cite: 42].",
        "personas": [
            {"nombre": "Maria Leida Bedoya", "doc": "25078205", "fecha": "25/08/1956", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1672", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Miralba Palechor - Prioridad baja (RUFE-1672)[cite: 42].",
        "personas": [
            {"nombre": "Miralba Palechor", "doc": "25694014", "fecha": "02/09/1979", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luis Palechor", "doc": "10567424", "fecha": "01/03/1982", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Karen Julioth Palechor", "doc": "1058786996", "fecha": "29/08/2006", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1673", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Omar Eduardo Marquez - Finca Ocaso, prioridad baja (RUFE-1673)[cite: 42].",
        "personas": [
            {"nombre": "Omar Eduardo Marquez", "doc": "16684182", "fecha": "18/04/1963", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Olga Lucia Sabogal", "doc": "4722260", "fecha": "07/12/1980", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Sluisa Fernanda Rojas", "doc": "1118289483", "fecha": "05/09/1988", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1660-1673...")
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
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE documento_identidad = %s", (p["doc"],))
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
        print(f"MIGRACIÓN LOTE 1660-1673 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
