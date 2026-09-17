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
        "num_formulario": "664", "corregimiento": "Buenos Aires", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con mampostería y muros afectados; se recomienda evacuar[cite: 64].",
        "personas": [
            {"nombre": "Sandra Liliana Insuasti Avila", "doc": "66828125", "fecha": "02/08/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Dina Marcela Romero Insuasti", "doc": "1118292891", "fecha": "27/12/1989", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "665", "corregimiento": "Buenos Aires", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras mínimas en mampostería. Habitable.",
        "personas": [
            {"nombre": "Luz Karime Muñoz", "doc": "1118301647", "fecha": "01/01/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "666", "corregimiento": "San Fernando", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras horizontales y verticales por desplazamiento de elementos.",
        "personas": [
            {"nombre": "Zorayda Polanco", "doc": "31468932", "fecha": "05/08/1961", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Eleida Gomez Cardona", "doc": "20558735", "fecha": "10/05/1931", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "667", "corregimiento": "San Fernando Pte Alto", "prioridad": "ALTA",
        "observaciones_evaluador": "Estructura de tercer piso descolgada y sujeta únicamente de listones; alto riesgo de colapso con recomendación de demolición parcial.",
        "personas": [
            {"nombre": "Maria Edilia Gonzalez", "doc": "29432540", "fecha": "10/05/1958", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jamerson Gonzalez", "doc": "16753755", "fecha": "20/10/1968", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "668", "corregimiento": "Laguna Seca", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con grietas en muros, conexión de viga y muro, además de asentamientos diferenciales y fisuras por desplazamiento[cite: 66].",
        "personas": [
            {"nombre": "Edgar Francisco Sanchez", "doc": "79589919", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alejandra Alouet", "doc": "29118338", "fecha": "01/01/1980", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Mariana Sanchez Alouet", "doc": "1232819163", "fecha": "01/01/2015", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "669", "corregimiento": "Las Vegas", "prioridad": "ALTA",
        "observaciones_evaluador": "Muros sin sistema de confinamiento, con grietas considerables y muros internos sueltos. Se recomienda demolición parcial.",
        "personas": [
            {"nombre": "Landily Johan Quiñones Quintero", "doc": "1118295800", "fecha": "26/02/1999", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "670", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en mampostería.",
        "personas": [
            {"nombre": "Oxy Pulman", "doc": "16603464", "fecha": "14/09/1947", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "671", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en mampostería del primer piso, se sugiere demoler el muro de la cocina.",
        "personas": [
            {"nombre": "Jenny Ordoñez", "doc": "66822814", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "672", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en pañete y muros por desplazamiento.",
        "personas": [
            {"nombre": "Omar Javier Gonzalez Corela", "doc": "16449037", "fecha": "20/04/1959", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "673", "corregimiento": "Las Vegas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con grietas en muros, desprendimiento de material en la parte trasera y asentamiento diferencial.",
        "personas": [
            {"nombre": "Luz Maria Cabrera", "doc": "31467626", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "674", "corregimiento": "La Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de 3 pisos con azotea y tejas de asbesto-cemento, paredes con fisuras y requerimiento de evaluación estructural por ingeniero calculista.",
        "personas": [
            {"nombre": "Maritza Viveros Garcia", "doc": "29978443", "fecha": "11/12/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "675", "corregimiento": "La Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de dos pisos con fisuras en muros estructurales del segundo piso y deformación en placas.",
        "personas": [
            {"nombre": "Manuel Francisco Calderon", "doc": "16705574", "fecha": "17/12/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nora Patricia Gutierrez", "doc": "31970910", "fecha": "11/04/1968", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 664-675...")
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
        print(f"MIGRACIÓN LOTE 664-675 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
