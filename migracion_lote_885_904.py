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
        "num_formulario": "885", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda evaluada con prioridad baja.",
        "personas": [
            {"nombre": "Luis Alberto Vargas", "doc": "6551156", "fecha": "07/07/1958", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Eva Sierra", "doc": "31525231", "fecha": "17/05/1964", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "886", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble evaluado con prioridad baja.",
        "personas": [
            {"nombre": "Marcos Atterhortua Fajardo", "doc": "1006536023", "fecha": "22/05/2002", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Dayana Payana", "doc": "1004301110", "fecha": "28/09/2002", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "887", "corregimiento": "Las Cruces", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda verificada sin novedades críticas mayores.",
        "personas": [
            {"nombre": "Luz Adriana Rivera", "doc": "29973229", "fecha": "12/10/1983", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jesus David Rivera", "doc": "1192916751", "fecha": "14/12/2010", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Luis Eduardo Molano", "doc": "2191216406", "fecha": "16/06/2010", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Gabriela Molano", "doc": "1116383454", "fecha": "05/01/2021", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "888", "corregimiento": "Buitrera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisura en terreno y deslizamientos tendientes a requerir obras de contención.",
        "personas": [
            {"nombre": "Silvio Julio Forero Mejia", "doc": "14959010", "fecha": "26/08/1946", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jermy Andrea Forero", "doc": "66999153", "fecha": "28/05/1977", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Iker Gerard Forero", "doc": "1232794218", "fecha": "09/09/2015", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "889", "corregimiento": "Las Cruces", "prioridad": "MEDIA",
        "observaciones_evaluador": "Edificación rudimentaria en madera y zinc; habita una sola persona dedicada al reciclaje.",
        "personas": [
            {"nombre": "Luz Maria Monroy", "doc": "31969189", "fecha": "31/05/1963", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "890", "corregimiento": "Las Cruces", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda inspeccionada con prioridad media.",
        "personas": [
            {"nombre": "Mory Hidalgo", "doc": "31262535", "fecha": "25/08/1953", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "891", "corregimiento": "Las Cruces", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda calificada con Riesgo Alto por daños severos y condiciones de habitabilidad comprometidas.",
        "personas": [
            {"nombre": "Marbiyeth Gomez", "doc": "1143868470", "fecha": "10/10/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Lisa Victoria Morales Gomez", "doc": "1118314197", "fecha": "02/06/2025", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "892", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de bahareque con muros colapsados.",
        "personas": [
            {"nombre": "Juan Livinof Yanten Tulande", "doc": "2693190", "fecha": "01/01/1935", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Liliana Yanten", "doc": "0", "fecha": "01/01/1968", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "893", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Afectaciones de gran dimensión a lo largo de la vivienda en mampostería, con talud en alto riesgo.",
        "personas": [
            {"nombre": "Antidio Hoyos Galindez", "doc": "76334859", "fecha": "26/01/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Cielo Valencia", "doc": "31480649", "fecha": "22/11/1978", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Jaider Santiago Hoyos", "doc": "0", "fecha": "11/12/2002", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "894", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con muros y losas premoldeadas con riesgo de colapso, terreno asentado.",
        "personas": [
            {"nombre": "Edaddstramoroo Semerel", "doc": "14976409", "fecha": "13/10/1951", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Marta Elena Segura Murcia", "doc": "31902906", "fecha": "05/05/1961", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Jose Fernando Segura Murcia", "doc": "16760682", "fecha": "12/03/1959", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "895", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con requerimiento de reparaciones en muros y daños menores.",
        "personas": [
            {"nombre": "Erika Alexandra Pabun Muñoz", "doc": "1118296361", "fecha": "26/06/1991", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Richard Orozco Pabun", "doc": "1116374811", "fecha": "21/11/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Avis Andez Garcia Oviedo", "doc": "1118290454", "fecha": "18/11/1982", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "896", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble evaluado con prioridad baja.",
        "personas": [
            {"nombre": "Edilmer Alvarez", "doc": "1061987538", "fecha": "04/08/1997", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yadi Dayana Gomez", "doc": "1007359933", "fecha": "14/10/1999", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Andy Matias Alvarez Gomez", "doc": "1105934943", "fecha": "08/02/2019", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Maylin Dayeli Alvarez Gomez", "doc": "1232817294", "fecha": "26/08/2021", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "897", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Inspección estructural completada con prioridad baja.",
        "personas": [
            {"nombre": "Ramiro Rengifo Gomez", "doc": "4620600", "fecha": "20/03/1948", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "898", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado con prioridad baja.",
        "personas": [
            {"nombre": "Danilo Cruz Meneses", "doc": "16456463", "fecha": "16/04/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "899", "corregimiento": "Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de dos niveles con reporte de fisuras y daños menores en mampostería no estructural[cite: 69].",
        "personas": [
            {"nombre": "Maria Fernanda Bustos Herrera", "doc": "1023915020", "fecha": "24/02/1992", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sara Julieta Sanchez", "doc": "1021683030", "fecha": "15/08/2010", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Tomas Geronimo Sanchez", "doc": "1016741146", "fecha": "27/06/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "900", "corregimiento": "Estancia Vieja", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble evaluado con prioridad media tras sismo.",
        "personas": [
            {"nombre": "Isabel Hernandez", "doc": "118298562", "fecha": "01/01/1992", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cristian Garcia", "doc": "128294843", "fecha": "24/10/1990", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Valeria Garcia Hernandez", "doc": "1104833026", "fecha": "16/07/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Santiago Garcia Hernandez", "doc": "1232805225", "fecha": "29/05/2018", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Maria Alejandra Garcia", "doc": "1104839279", "fecha": "01/08/2016", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "901", "corregimiento": "Nueva Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda calificada con Riesgo Alto por daños significativos en elementos portantes.",
        "personas": [
            {"nombre": "Leonor Garcia", "doc": "29973441", "fecha": "07/09/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cristian Cardona", "doc": "1041610477", "fecha": "26/03/1987", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Laura Isabel Cardona", "doc": "0", "fecha": "14/04/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Maria Cristina Martinez", "doc": "0", "fecha": "07/05/1953", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Daniel Ruiz", "doc": "0", "fecha": "22/08/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "902", "corregimiento": "Salazar", "prioridad": "ALTA",
        "observaciones_evaluador": "Inmueble con reporte de afectación alta y requerimiento de inspección especializada.",
        "personas": [
            {"nombre": "Maria Lucy Giraldo Jaramillo", "doc": "66712679", "fecha": "01/03/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alfredo Zuñiga", "doc": "16448300", "fecha": "21/03/1960", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "903", "corregimiento": "Estancia Vieja", "prioridad": "ALTA",
        "observaciones_evaluador": "Inmueble con reporte de afectación estructural evaluado con prioridad alta.",
        "personas": [
            {"nombre": "Alfonso Lopes", "doc": "79712297", "fecha": "17/03/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Alejandra Gudiño", "doc": "6019351", "fecha": "07/05/1987", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Efin Gudiño", "doc": "0", "fecha": "20/10/2007", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "904", "corregimiento": "Nueva Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Paredes inclinadas, grietas considerables y techos averiados.",
        "personas": [
            {"nombre": "Lua Myriam Guevara Alvarez", "doc": "66979696", "fecha": "03/01/1974", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jessica Fernanda Hernandez Alvarez", "doc": "1118295865", "fecha": "16/05/1991", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Camilo Gallego Guevara", "doc": "1118260337", "fecha": "08/10/1997", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ezequiel Hernandez Guevara", "doc": "1104844849", "fecha": "23/02/2019", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Shou Alexandro Hernandez Guevara", "doc": "1143884070", "fecha": "27/02/2024", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Duvan David Guevara", "doc": "1110284715", "fecha": "23/04/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jose Miguel Guevara", "doc": "6137822", "fecha": "05/05/1946", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 885-904...")
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
        print(f"MIGRACIÓN LOTE 885-904 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
