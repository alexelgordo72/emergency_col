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
        "num_formulario": "847", "corregimiento": "Rincón Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con afectaciones moderadas en mampostería y acabados.",
        "personas": [
            {"nombre": "Oscar Marcela Guerrero Ortiz", "doc": "87247073", "fecha": "21/02/1973", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "848", "corregimiento": "Rincón Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda rural con afectación moderada en estructura y mampostería.",
        "personas": [
            {"nombre": "Ismael Gomez Gomez", "doc": "1821247", "fecha": "13/08/1946", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Francelia de Gomez", "doc": "27148891", "fecha": "02/11/1952", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "849", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras mínimas y mampostería supervisada.",
        "personas": [
            {"nombre": "Diego Fernando Garcia Erazo", "doc": "1118293642", "fecha": "17/09/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Laura Isabel Serna", "doc": "1004518614", "fecha": "29/01/1997", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Gabriela Serna Garcia", "doc": "0", "fecha": "24/02/2021", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "850", "corregimiento": "Dapa Miravalle", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con sistema estructural destruido, alto riesgo de colapso.",
        "personas": [
            {"nombre": "Marco Ocampo Barrios", "doc": "16461728", "fecha": "19/02/1981", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Joaquin Mario Lopez", "doc": "16455419", "fecha": "18/11/1974", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Camilo Bolove Santos", "doc": "1107061890", "fecha": "25/12/1988", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "851", "corregimiento": "Alto Dapa Getsemani", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en madera con averías menores.",
        "personas": [
            {"nombre": "Jorge Luis Rojas", "doc": "4895628", "fecha": "03/06/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Rita Tovar Rojas", "doc": "26529080", "fecha": "25/06/1967", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Walter Smith Tovar Rojas", "doc": "7055073", "fecha": "10/03/1991", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "852", "corregimiento": "Rincon Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras mínimas en mampostería.",
        "personas": [
            {"nombre": "Laura Valentina Rasero Arce", "doc": "1007045844", "fecha": "17/11/1998", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "853", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con daños graves en mampostería y estructura de soporte[cite: 69].",
        "personas": [
            {"nombre": "Apolinar Muñoz Gutierrez", "doc": "94450328", "fecha": "20/10/1969", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Derly Tatiana Muñoz", "doc": "0", "fecha": "15/10/1999", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "854", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Alto riesgo por deslizamiento en masa y afectación severa en muros.",
        "personas": [
            {"nombre": "Freddy Grovany Bolaños", "doc": "16887892", "fecha": "28/06/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Patricia Yaneth Guevara", "doc": "1144133094", "fecha": "02/01/1990", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Johana Bolaños", "doc": "1006436760", "fecha": "06/07/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Lian David Bolaños", "doc": "1232841950", "fecha": "01/01/2026", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "855", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con fisuras severas en muros y mampostería comprometida por asentamiento.",
        "personas": [
            {"nombre": "Ana Cristina Lemos Muñoz", "doc": "66997212", "fecha": "15/04/1977", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "856", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con elementos estructurales comprometidos y riesgo de colapso inminente.",
        "personas": [
            {"nombre": "Teresa Gomez Gomez", "doc": "66854902", "fecha": "11/04/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Karen Tatiana Velasco", "doc": "1007632285", "fecha": "21/02/2002", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Rodrigo Hernan Velazco", "doc": "94429187", "fecha": "04/05/1975", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Juan Camilo Velazco", "doc": "1118307526", "fecha": "21/02/1996", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "857", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con fisuras graves en mampostería y riesgo de colapso.",
        "personas": [
            {"nombre": "Medardo Mañoz", "doc": "94374024", "fecha": "22/12/1976", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "858", "corregimiento": "Santa Ines", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado con fisuras superficiales menores[cite: 70].",
        "personas": [
            {"nombre": "Rodrigo Agredo Santamaria", "doc": "76446257", "fecha": "30/08/1957", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yanelis Torres Pineda", "doc": "29176287", "fecha": "25/02/1979", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Laura Daniela Torres", "doc": "1006435772", "fecha": "15/05/2000", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "859", "corregimiento": "Santa Ines", "prioridad": "BAJA",
        "observaciones_evaluador": "Inspección completada con prioridad baja.",
        "personas": [
            {"nombre": "Norma Angelica Paredes Gaviria", "doc": "2958194", "fecha": "12/01/1971", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sara Montilla", "doc": "1107849704", "fecha": "30/09/2007", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "860", "corregimiento": "Santa Ines", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda verificada sin afectaciones mayores.",
        "personas": [
            {"nombre": "Javier Caroldo", "doc": "16425467", "fecha": "28/11/1952", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "861", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Desprendimiento de muro en el cuarto de por asentamiento.",
        "personas": [
            {"nombre": "Alejandre Hincapie", "doc": "1006537343", "fecha": "05/07/2003", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "862", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en fachada, desprendimiento de repello.",
        "personas": [
            {"nombre": "Dinara Isabel Candelo", "doc": "29974244", "fecha": "14/11/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "863", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble revisado con prioridad baja.",
        "personas": [
            {"nombre": "Dolfay Amparo Charria", "doc": "31193887", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "864", "corregimiento": "Casco Urbano", "prioridad": "BAJA",
        "observaciones_evaluador": "Grietas en muros por asentamiento, dilatación en juntas.",
        "personas": [
            {"nombre": "Edilmo Del", "doc": "25200504", "fecha": "09/05/1949", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "865", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fracturas en muros estructurales y grietas en baldosas por asentamiento diferencial[cite: 71].",
        "personas": [
            {"nombre": "Gevarelo Pantoja", "doc": "5291626", "fecha": "10/10/1950", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "866", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Columna con fisuras y separación entre elementos estructurales.",
        "personas": [
            {"nombre": "Dory Cordoba Muñoz", "doc": "31465932", "fecha": "31/03/1957", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "867", "corregimiento": "Madre Selva", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muros con grietas longitudinales y asentamiento.",
        "personas": [
            {"nombre": "Maria Emma Priza", "doc": "29581636", "fecha": "01/04/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "868", "corregimiento": "Santa Ines", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inspección rural completada con observaciones técnicas.",
        "personas": [
            {"nombre": "Hector Armando Rojas Calderon", "doc": "17781060", "fecha": "31/10/1946", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "869", "corregimiento": "Santa Ines", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inspección completada en sector rural.",
        "personas": [
            {"nombre": "Selene Quintero Vivas", "doc": "31475423", "fecha": "19/10/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luis Hernando Cortez Quintero", "doc": "3216955976", "fecha": "24/08/1961", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Fredy Moreno", "doc": "19015903", "fecha": "05/12/1984", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "870", "corregimiento": "Santa Ines", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras superficiales en muros.",
        "personas": [
            {"nombre": "Graciela Zapata Loaiza", "doc": "31467431", "fecha": "18/02/1959", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Danilo Marquez", "doc": "16449063", "fecha": "02/07/1960", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Daniela Marquez", "doc": "1118305032", "fecha": "10/08/1995", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "871", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grietas con desprendimiento en techo.",
        "personas": [
            {"nombre": "Hautar Santamaria Salcedo", "doc": "16445850", "fecha": "19/01/1954", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "872", "corregimiento": "Belalcazar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras horizontales y verticales por desprendimiento en muros.",
        "personas": [
            {"nombre": "Alivio Edith Rojas Doza", "doc": "29738375", "fecha": "20/11/1957", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Martin X", "doc": "16728592", "fecha": "23/08/1966", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "873", "corregimiento": "Guadalupe", "prioridad": "ALTA",
        "observaciones_evaluador": "Losas con cables de flexión y predecible afectación estructural que requiere intervención de especialista[cite: 72].",
        "personas": [
            {"nombre": "Carlos Rafael Boiga", "doc": "14590901", "fecha": "23/02/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "874", "corregimiento": "Guadalupe", "prioridad": "ALTA",
        "observaciones_evaluador": "Desprendimiento grave de repello y muro estructural profundamente comprometido[cite: 72].",
        "personas": [
            {"nombre": "Kelly Yurani Caicedo", "doc": "1118258858", "fecha": "03/11/1993", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 847-874...")
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
        print(f"MIGRACIÓN LOTE 847-874 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
