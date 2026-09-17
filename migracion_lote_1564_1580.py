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
        "num_formulario": "1564", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Alexander Zuasa Cardona - Apto 101 en edificio de 5 pisos con fisuras en placas, se recomienda evaluación especializada (RUFE-1564)[cite: 51].",
        "personas": [
            {"nombre": "Alexander Zuasa Cardona", "doc": "94296683", "fecha": "20/11/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diana Ximena Garcia Rodriguez", "doc": "25171772", "fecha": "19/01/1977", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Elieser Amanuel Garcia", "doc": "94402786", "fecha": "10/09/1973", "es_jefe": False, "sexo": "M", "parentesco": "Familiar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1565", "corregimiento": "Las Cruces", "prioridad": "BAJA",
        "observaciones_evaluador": "Martha Solano - Sin afectaciones visibles, hacer seguimiento (RUFE-1565)[cite: 52].",
        "personas": [
            {"nombre": "Martha Solano", "doc": "314782661", "fecha": "10/08/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1566", "corregimiento": "San Fernando", "prioridad": "BAJA",
        "observaciones_evaluador": "Ingrid Paz - Sin afectaciones visibles, hacer seguimiento (RUFE-1566)[cite: 52].",
        "personas": [
            {"nombre": "Ingrid Paz", "doc": "1119288586", "fecha": "14/03/1988", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1567", "corregimiento": "San Fernando", "prioridad": "BAJA",
        "observaciones_evaluador": "Luz Nelly Quintero Calderon - Sin afectaciones visibles (RUFE-1567)[cite: 52].",
        "personas": [
            {"nombre": "Luz Nelly Quintero Calderon", "doc": "31470095", "fecha": "12/01/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1568", "corregimiento": "San Fernando", "prioridad": "BAJA",
        "observaciones_evaluador": "Monica Muñoz - Sin afectaciones visibles (RUFE-1568)[cite: 52].",
        "personas": [
            {"nombre": "Monica Muñoz", "doc": "331476360", "fecha": "22/02/1973", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1569", "corregimiento": "San Fernando", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Margarita Beoritica Fernandez - Sin afectaciones visibles (RUFE-1569)[cite: 52].",
        "personas": [
            {"nombre": "Maria Margarita Beoritica Fernandez", "doc": "31476594", "fecha": "29/08/1971", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1570", "corregimiento": "Buenos Aires", "prioridad": "BAJA",
        "observaciones_evaluador": "Maliza Lugo Beltran - Sin afectaciones visibles (RUFE-1570)[cite: 52].",
        "personas": [
            {"nombre": "Maliza Lugo Beltran", "doc": "1118292192", "fecha": "08/08/1989", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1571", "corregimiento": "Buenos Aires", "prioridad": "BAJA",
        "observaciones_evaluador": "Edel Nieto - Sin afectaciones visibles (RUFE-1571)[cite: 53].",
        "personas": [
            {"nombre": "Edel Nieto", "doc": "31477929", "fecha": "01/01/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1572", "corregimiento": "Buenos Aires", "prioridad": "BAJA",
        "observaciones_evaluador": "Ana Luisa Ortega - Sin afectaciones visibles (RUFE-1572)[cite: 53].",
        "personas": [
            {"nombre": "Ana Luisa Ortega", "doc": "31475773", "fecha": "19/11/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1573", "corregimiento": "Guabinas - Filandia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Deviison Puente Osorio - Torre 2, Apto 103 inspeccionado (RUFE-1573)[cite: 53].",
        "personas": [
            {"nombre": "Deviison Puente Osorio", "doc": "6550797", "fecha": "14/10/1985", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gladis Osorio", "doc": "31469995", "fecha": "16/11/1959", "es_jefe": False, "sexo": "F", "parentesco": "Padre/Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1574", "corregimiento": "Pizarro", "prioridad": "BAJA",
        "observaciones_evaluador": "Luz Adriana Osorio - Hogar ICBF, adecuaciones y seguimiento (RUFE-1574)[cite: 53].",
        "personas": [
            {"nombre": "Luz Adriana Osorio", "doc": "66973808", "fecha": "01/01/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1575", "corregimiento": "Pizarro", "prioridad": "BAJA",
        "observaciones_evaluador": "Karen Dayana Pedroza Osorio - Sin afectaciones visibles (RUFE-1575)[cite: 53].",
        "personas": [
            {"nombre": "Karen Dayana Pedroza Osorio", "doc": "11441875569", "fecha": "18/07/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1576", "corregimiento": "Capuliños - Pizarro", "prioridad": "BAJA",
        "observaciones_evaluador": "Oneida Alicia Gomez - Afectaciones menores, fisuras (RUFE-1576)[cite: 53].",
        "personas": [
            {"nombre": "Oneida Alicia Gomez", "doc": "39831625", "fecha": "24/11/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1577", "corregimiento": "Las Cruces", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Isabel Tarquino - Afectaciones menores, fisuras y dilataciones (RUFE-1577)[cite: 53].",
        "personas": [
            {"nombre": "Maria Isabel Tarquino", "doc": "29975835", "fecha": "09/07/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1578", "corregimiento": "Las Cruces", "prioridad": "BAJA",
        "observaciones_evaluador": "Alexandra Trullo - Sin afectaciones visibles (RUFE-1578)[cite: 53].",
        "personas": [
            {"nombre": "Alexandra Trullo", "doc": "31481768", "fecha": "28/07/1979", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1579", "corregimiento": "Pizarro", "prioridad": "BAJA",
        "observaciones_evaluador": "Lina Marcela Lopez Mosquera - Sin afectaciones visibles (RUFE-1579)[cite: 53].",
        "personas": [
            {"nombre": "Lina Marcela Lopez Mosquera", "doc": "1006072519", "fecha": "16/02/2000", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1580", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Habiola Rivera - Sin afectaciones visibles (RUFE-1580)[cite: 53].",
        "personas": [
            {"nombre": "Habiola Rivera", "doc": "31476092", "fecha": "15/10/1940", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1564-1580...")
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
        print(f"MIGRACIÓN LOTE 1564-1580 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
