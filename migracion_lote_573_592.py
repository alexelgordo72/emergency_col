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
        "num_formulario": "573", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales leves en el segundo piso. Sin novedad mayor[cite: 67].",
        "personas": [
            {"nombre": "Diana Lorena Lopez", "doc": "29973311", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "574", "corregimiento": "Arroyohondo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en el piso superior y desprendimiento parcial de revestimiento. Medianamente habitable[cite: 67].",
        "personas": [
            {"nombre": "How nao Bedya", "doc": "1026258813", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "576", "corregimiento": "Mulalo", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras menores en muros y mampostería. Habitable sin riesgo latente[cite: 68].",
        "personas": [
            {"nombre": "Luz Aida Basten Barco", "doc": "68985788", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "577", "corregimiento": "Buitrera", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras leves en muros y puertas/ventanas. Habitable[cite: 68].",
        "personas": [
            {"nombre": "Carlos Cuero Garcia", "doc": "1114448279", "fecha": "29/04/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andrea Hernandez", "doc": "1118301122", "fecha": "23/08/1993", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Frank Quero Hernandez", "doc": "1109926936", "fecha": "13/09/2012", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "581", "corregimiento": "Laguna Seca", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con grietas en muros y en fachada; asentamiento diferencial en el terreno. Se recomienda diagnóstico de especialista[cite: 69].",
        "personas": [
            {"nombre": "Jhon Obando Londoño", "doc": "11319074", "fecha": "02/07/1971", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Teresa Cuarta Marin", "doc": "31951332", "fecha": "16/08/1966", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Marta Paula Obando Cuarta", "doc": "1117842989", "fecha": "24/02/2006", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "582", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con mampostería comprometida en un 80% y riesgo latente de colapso[cite: 69].",
        "personas": [
            {"nombre": "Rubiela Galindez", "doc": "31469581", "fecha": "14/05/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "586", "corregimiento": "Santa Ines", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de 3 pisos con muros agrietados y caídos, rotura de vidrio. Requiere reforzamiento estructural[cite: 70].",
        "personas": [
            {"nombre": "Juan Elico Chavez C.", "doc": "14955448", "fecha": "05/06/1949", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "587", "corregimiento": "Santa Ines", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda rural de 3 pisos con sótano, construida de forma artesanal; daños severos por sismo, muros caídos y alta vulnerabilidad. Inhabitable con recomendación de desalojo inmediato[cite: 70].",
        "personas": [
            {"nombre": "Jhon Alexander Burgo", "doc": "16940570", "fecha": "16/06/1947", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Margot Montero", "doc": "1144039988", "fecha": "08/08/1961", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Michel Montero", "doc": "1116378370", "fecha": "14/11/2005", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "591", "corregimiento": "Santa Ines", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda rural de mampostería con fisuras en juntas de muro y desplome parcial de elementos no estructurales[cite: 71].",
        "personas": [
            {"nombre": "Nora Cumea Garcia", "doc": "38964875", "fecha": "14/12/1944", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Angel Camilo Castro", "doc": "111036640", "fecha": "12/02/2006", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "592", "corregimiento": "La Pica", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda rural con afectaciones en mampostería no estructural y fisuras por asentamiento en el piso[cite: 71].",
        "personas": [
            {"nombre": "Edgar A. Pomar", "doc": "14941559", "fecha": "14/08/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gloria Edilia Herrera", "doc": "24412294", "fecha": "07/11/1946", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Fabiana Herrera", "doc": "29156496", "fecha": "01/01/1982", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 573-592...")
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
        print(f"MIGRACIÓN LOTE 573-592 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
