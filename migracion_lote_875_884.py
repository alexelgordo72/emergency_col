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
        "num_formulario": "875", "corregimiento": "Belalcazar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con afectaciones moderadas y fisuras en mampostería no confinada[cite: 67].",
        "personas": [
            {"nombre": "Angela Filigrana Velazco", "doc": "31470390", "fecha": "10/03/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jemes Filigrana", "doc": "16452727", "fecha": "07/10/1963", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "876", "corregimiento": "Belalcazar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con fisuras en muros y mampostería afectada[cite: 67].",
        "personas": [
            {"nombre": "Ayron Flores Giron", "doc": "16458974", "fecha": "28/09/1979", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jhon Jairo", "doc": "31485664", "fecha": "27/03/1981", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Natalia Andica Carmona", "doc": "1107836792", "fecha": "16/09/2004", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "877", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras superficiales y separaciones menores en juntas[cite: 67].",
        "personas": [
            {"nombre": "Pablo Andres Rojas Vargas", "doc": "1114897780", "fecha": "17/08/1997", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Marjuri Ortiz", "doc": "1193265580", "fecha": "25/12/2001", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "878", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con fisuras en muros y asentamiento controlado[cite: 68].",
        "personas": [
            {"nombre": "Doris del Carmen Pulidor", "doc": "29116549", "fecha": "07/07/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Brayan Fernando Valencia", "doc": "707840761", "fecha": "16/08/2001", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "879", "corregimiento": "Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras estructurales y seguimiento prioritario[cite: 68].",
        "personas": [
            {"nombre": "Maria Lilia Granados", "doc": "29976097", "fecha": "20/12/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "880", "corregimiento": "Nueva Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble evaluado con fisuras en mampostería y acabados[cite: 68].",
        "personas": [
            {"nombre": "Juan Carlos Chontre", "doc": "16791668", "fecha": "24/10/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Karen Tatiana Chontre", "doc": "1193447656", "fecha": "12/09/2000", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Carlos Chontre Ceron", "doc": "7007619614", "fecha": "19/07/2003", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Brandon Steven Chontre Ceron", "doc": "1108254453", "fecha": "13/05/2007", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "881", "corregimiento": "Nueva Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de material con revisión estructural completada.",
        "personas": [
            {"nombre": "Domorys Delgado", "doc": "31424921", "fecha": "28/01/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "882", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras en muros por asentamiento diferencial[cite: 68].",
        "personas": [
            {"nombre": "Omar Ortiz", "doc": "65218128", "fecha": "09/11/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Mary del Carmen Mueses", "doc": "31488042", "fecha": "24/05/1993", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Estefania Mueses", "doc": "1116379075", "fecha": "15/06/2015", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Elizabeth Mueses", "doc": "1116381224", "fecha": "15/08/2017", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "883", "corregimiento": "Comfandi", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con prioridad baja verificado.",
        "personas": [
            {"nombre": "Jenin Yilema Arboleda", "doc": "16890951", "fecha": "20/08/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gladis Velasco", "doc": "99507290", "fecha": "31/05/1979", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Hyon Arboleda", "doc": "1006036141", "fecha": "17/05/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "884", "corregimiento": "Las Américas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con daños significativos en elementos de soporte y mampostería; riesgo alto[cite: 69].",
        "personas": [
            {"nombre": "Fabian Montoya", "doc": "16454871", "fecha": "24/03/1974", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Natalia Montoya", "doc": "1006054364", "fecha": "12/06/2007", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Roxcs Hernandez Montoya", "doc": "1118313351", "fecha": "19/12/2022", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 875-884...")
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
        print(f"MIGRACIÓN LOTE 875-884 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
