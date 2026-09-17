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
    # --- LOS FALTANTES (116 al 120) ---
    {
        "num_formulario": "116", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averías en paredes y piso.",
        "personas": [
            {"nombre": "Maria Helena Ocampo", "doc": "31472815", "fecha": "07/10/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Isabel Jaramillo", "doc": "66712035", "fecha": "12/05/1970", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "117", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averías en estructura compleja y conjunto lesional.",
        "personas": [
            {"nombre": "Marianela Marmolejo", "doc": "31171792", "fecha": "12/10/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "118", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averías en paredes y baño.",
        "personas": [
            {"nombre": "Roberth Plaza", "doc": "16462012", "fecha": "12/07/1981", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andrea Vargas", "doc": "66972935", "fecha": "15/04/1976", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Sofia Plaza Vargas", "doc": "142057393", "fecha": "12/12/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jacobo Plaza Vargas", "doc": "112061387", "fecha": "08/01/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "119", "corregimiento": "Alto Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averías en paredes.",
        "personas": [
            {"nombre": "Francy Johanna Buitrago", "doc": "33945399", "fecha": "28/02/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juliana Esquivel", "doc": "1116372729", "fecha": "09/10/2005", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "120", "corregimiento": "Alto Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averías en puerta y piso.",
        "personas": [
            {"nombre": "Jean Alexander Yace", "doc": "76290498", "fecha": "15/04/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nubia Milena Lopez", "doc": "24853131", "fecha": "15/01/1977", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Daniela Lopez", "doc": "1006110849", "fecha": "25/03/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ismelda Lopez", "doc": "25085730", "fecha": "05/01/1949", "es_jefe": False, "sexo": "F", "parentesco": "Abuelo(a)", "etnia": "Ninguna"},
            {"nombre": "Anna Maria Yace Lopez", "doc": "1116374724", "fecha": "17/12/2008", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Dannia Sofia Yace Lopez", "doc": "148341861", "fecha": "10/10/2021", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },

    # --- LOTE 121-126 (Para asegurar cobertura total) ---
    {
        "num_formulario": "121", "corregimiento": "Alto Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averías en paredes y columnas.",
        "personas": [
            {"nombre": "Sara Cifuentes", "doc": "1006537121", "fecha": "12/06/1997", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andres Felipe Calvo", "doc": "1144178906", "fecha": "17/07/1995", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Ariana Calvo Cifuentes", "doc": "11232829011", "fecha": "17/12/2023", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "122", "corregimiento": "Miravalle Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Vivienda en construcción, obra negra. Partes afectadas.",
        "personas": [
            {"nombre": "Carlos Arturo Verdugo", "doc": "16448381", "fecha": "13/12/1956", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carmen Rosa Quintero", "doc": "38942161", "fecha": "29/06/1956", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "124", "corregimiento": "Alto Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averías en construcción, paredes bahareque.",
        "personas": [
            {"nombre": "Dania Quintero", "doc": "1118305345", "fecha": "06/03/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Layonner Muñoz", "doc": "1116377144", "fecha": "29/09/2013", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Yuberney Martinez", "doc": "11121495724", "fecha": "28/07/1992", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Wendy Rojas", "doc": "112875520", "fecha": "04/01/2016", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "126", "corregimiento": "Alto Dapa", "prioridad": "LEVE",
        "observaciones_evaluador": "Averías en pañetes.",
        "personas": [
            {"nombre": "Blanca Mireya Diaz", "doc": "1118285161", "fecha": "15/02/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alexander Ipia", "doc": "4646708", "fecha": "07/09/1980", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Cesar Diaz", "doc": "1005991522", "fecha": "27/09/2003", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jose Nolbey Diaz", "doc": "2693439", "fecha": "01/12/1965", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Patricia Vargas", "doc": "63990686", "fecha": "20/01/1992", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL (Lote 116-126 completo)...")
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
        print(f"MIGRACIÓN LOTE 116-126 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
