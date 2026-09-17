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
        "num_formulario": "689", "corregimiento": "Buenos Aires", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de material con cubierta de concreto pandea, muro estructural expuesto, fracturado en la parte delantera; alto riesgo de colapso con recomendación de desalojo[cite: 71].",
        "personas": [
            {"nombre": "Sara Montenegro Gutierrez", "doc": "1110045603", "fecha": "23/06/2000", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Mauris Gutierrez Campo", "doc": "31976841", "fecha": "19/04/1968", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "690", "corregimiento": "Buenos Aires", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras en muros, desprendimientos y colapso parcial de paredes en la habitación de bahareque.",
        "personas": [
            {"nombre": "Katherine Zuñiga Mejia", "doc": "38464065", "fecha": "07/05/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Anderson Polindara", "doc": "7143857634", "fecha": "01/01/1999", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Sebastian Balensuela", "doc": "1105361053", "fecha": "01/06/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "691", "corregimiento": "Buenos Aires", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 3 pisos en material con grietas en muros y colapso parcial de mampostería; habitantes debieron desalojar provisionalmente.",
        "personas": [
            {"nombre": "Antonio Jose Lopez Gonzales", "doc": "17528935", "fecha": "28/05/1945", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yoni Blandon Oviedo", "doc": "1007779367", "fecha": "18/03/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Daniel Valdes Rodriguez", "doc": "1110591176", "fecha": "11/06/1998", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "692", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque colapsada, con desplome total de cubierta de madera y zinc. Orden de demolición[cite: 72].",
        "personas": [
            {"nombre": "Dulka Urrue de Leon", "doc": "29579400", "fecha": "31/12/1926", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "693", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque con alto riesgo de colapso en muros y cubierta de madera. Desplome total.",
        "personas": [
            {"nombre": "Rubeito Arturo Carmona", "doc": "4415112", "fecha": "23/10/1945", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Miryam Rosero", "doc": "25542972", "fecha": "12/05/1951", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "694", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con colapso estructural, cocina destruida y muros perimetrales desplomados.",
        "personas": [
            {"nombre": "Maria Julia Leon", "doc": "29580927", "fecha": "22/04/1961", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "695", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con fisuras en mampostería y desplazamiento vertical en muros.",
        "personas": [
            {"nombre": "Liliana Gutierrez", "doc": "1060103454", "fecha": "27/01/2009", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jessica Cabiche Gutierrez", "doc": "1058729293", "fecha": "08/08/1986", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Deisy Lorena Cabiche Gutierrez", "doc": "1058729045", "fecha": "27/03/2007", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jose Moises Cabiche Concha", "doc": "1060201589", "fecha": "01/01/2012", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "696", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en material con asentamientos, desplazamiento de muros y losa fracturada con grieta transversal.",
        "personas": [
            {"nombre": "Carlos Andres Pipicano", "doc": "1130597819", "fecha": "19/05/1978", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juliana Giraldo", "doc": "31643216", "fecha": "01/01/1995", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "697", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con daños en el taller y parte baja, desprendimiento de muros por falta de columnas y grietas pronunciadas en placas causadas por desplazamiento.",
        "personas": [
            {"nombre": "Nosy Margot Parraex", "doc": "31482989", "fecha": "11/12/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 689-697...")
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
        print(f"MIGRACIÓN LOTE 689-697 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
