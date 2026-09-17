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
        "num_formulario": "1544", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Fernanda Martinez - Fisuras en panel yeso (RUFE-1544)[cite: 50].",
        "personas": [
            {"nombre": "Maria Fernanda Martinez", "doc": "66966701", "fecha": "19/07/1977", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1545", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Diana Marcela Polanco Astaiza - Fisuras en pisos, sin repello (RUFE-1545)[cite: 50].",
        "personas": [
            {"nombre": "Diana Marcela Polanco Astaiza", "doc": "1118304990", "fecha": "14/08/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1546", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Najar Softy Zuleta Muñoz - Inmueble residencial verificado (RUFE-1546)[cite: 50].",
        "personas": [
            {"nombre": "Najar Softy Zuleta Muñoz", "doc": "31629497", "fecha": "27/12/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1547", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Tatiana Ome Mera - Fisuras en muros, daños en baño (RUFE-1547)[cite: 50].",
        "personas": [
            {"nombre": "Tatiana Ome Mera", "doc": "1118304339", "fecha": "26/04/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1548", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Elizabeth Martinez Galarza - Cielorraso de esterilla y arena sostenido con tablas y guaduas, adulto mayor (RUFE-1548)[cite: 51].",
        "personas": [
            {"nombre": "Elizabeth Martinez Galarza", "doc": "38437032", "fecha": "23/03/1956", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jahouardo Jesus Viña Solis", "doc": "5447024", "fecha": "11/05/1967", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Carmen Vivas Martinez", "doc": "31474269", "fecha": "14/08/1963", "es_jefe": False, "sexo": "F", "parentesco": "Familiar", "etnia": "Ninguna"},
            {"nombre": "Diego Fernando Delgado", "doc": "16457588", "fecha": "23/03/1974", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1549", "corregimiento": "Estancia Vieja", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jose Donic Basto Gomez y Rosa Maria Mongel - Vivienda de 1 piso con fisuras en muros, posible deslizamiento (RUFE-1549)[cite: 51].",
        "personas": [
            {"nombre": "Jose Donic Basto Gomez", "doc": "219208", "fecha": "26/11/1955", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Rosa Maria Mongel", "doc": "28253958", "fecha": "03/12/1956", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1550", "corregimiento": "Pizarro", "prioridad": "MEDIA",
        "observaciones_evaluador": "Paya Loma / Berta Arango Londoño - Inmueble con fisuras en pisos y muros (RUFE-1550)[cite: 51].",
        "personas": [
            {"nombre": "Berta Arango Londoño", "doc": "1107845715", "fecha": "05/03/1952", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1551", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Sandra Eugenia Zamora Franco - Múltiples fracturas en paredes, cielos y techo, recomendación de reubicación preventiva (RUFE-1551)[cite: 52].",
        "personas": [
            {"nombre": "Sandra Eugenia Zamora Franco", "doc": "31998022", "fecha": "04/08/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ingrid Juliana Urrea Zamora", "doc": "1193075537", "fecha": "10/12/2001", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1552", "corregimiento": "Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Oscar Suarez y Leydi Sondobel Suarez - Vivienda de 1 piso con fisuras leves en muros (RUFE-1552)[cite: 53].",
        "personas": [
            {"nombre": "Oscar Suarez", "doc": "2647015", "fecha": "12/05/1940", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Leydi Sondobel Suarez", "doc": "1113309916", "fecha": "19/11/2015", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1553", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Maria Alejandra Nuries Barreger - Inmueble residencial con fisuras leves (RUFE-1553)[cite: 53].",
        "personas": [
            {"nombre": "Maria Alejandra Nuries Barreger", "doc": "1105683936", "fecha": "30/11/1992", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1544-1553...")
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
        print(f"MIGRACIÓN LOTE 1544-1553 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
