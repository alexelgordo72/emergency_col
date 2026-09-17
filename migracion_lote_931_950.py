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
        "num_formulario": "931", "corregimiento": "La Balastrera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grietas en el piso y daño de estructura soporte de la marquesina para secar café[cite: 71].",
        "personas": [
            {"nombre": "Emerita Morales Salamanca", "doc": "25295791", "fecha": "06/11/1963", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yuri Jhoana Imales Salamanca", "doc": "67043096", "fecha": "28/10/1985", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Isabela Yimeres Imales", "doc": "1108648124", "fecha": "04/01/2013", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Enriqueta Salamanca Imales", "doc": "25293928", "fecha": "31/12/1929", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "932", "corregimiento": "La Olga", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con desplome parcial y agrietamiento de muros.",
        "personas": [
            {"nombre": "Hugo Piamba Jinest", "doc": "16453859", "fecha": "09/07/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Rosalba Fernandez Ballos", "doc": "31971444", "fecha": "22/01/1968", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "933", "corregimiento": "La Olga", "prioridad": "ALTA",
        "observaciones_evaluador": "Beneficiadero de café afectado con daños en las estructuras que soportan la máquina y el techo.",
        "personas": [
            {"nombre": "Rodrigo Ruiz Galindez", "doc": "16450998", "fecha": "14/07/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Maria Rengifo Bueno", "doc": "31976867", "fecha": "16/02/1966", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Leidy Jhoana Ruiz Rengifo", "doc": "2107053314", "fecha": "05/02/1989", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "934", "corregimiento": "Santa Ines Peñas Negras", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con grietas en paredes y pisos.",
        "personas": [
            {"nombre": "Mision Estela Pechere Paban", "doc": "29581766", "fecha": "02/11/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Francisco Muñoz", "doc": "14984904", "fecha": "14/08/1952", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "935", "corregimiento": "Santa Ines El Chocho", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con muros apretados y verificación completada.",
        "personas": [
            {"nombre": "Mateo Roxs Herrera", "doc": "1114489907", "fecha": "16/06/1999", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Arquimedes Rojas Roa", "doc": "6095160", "fecha": "28/03/1943", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "936", "corregimiento": "Santa Ines", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras superficiales en mampostería.",
        "personas": [
            {"nombre": "Libia Velasco Delivers", "doc": "29580239", "fecha": "16/07/2026", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Hernan Holiveros Velasco", "doc": "6341741", "fecha": "27/05/2026", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "937", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Inmueble con reporte de caída de techo.",
        "personas": [
            {"nombre": "Jose Aquilino Marin Prado", "doc": "76296203", "fecha": "18/04/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "938", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con fisuras en paredes y desplome de muros en bahareque.",
        "personas": [
            {"nombre": "Diomidio Sanbon Imbachi", "doc": "6550011", "fecha": "27/07/1961", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "939", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con daños en paredes.",
        "personas": [
            {"nombre": "Dovon Holmiuon Alvarado", "doc": "16460033", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "940", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Inmueble con reporte de afectación alta y riesgo inminente.",
        "personas": [
            {"nombre": "Teodolfo Alvarado Sambani", "doc": "6342167", "fecha": "25/02/1969", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "941", "corregimiento": "Montañitas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado sin daños estructurales graves.",
        "personas": [
            {"nombre": "Pedro Pablo Gazon Prado", "doc": "6550039", "fecha": "25/10/1952", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "942", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con daños graves en mampostería y riesgo de colapso.",
        "personas": [
            {"nombre": "John Jairo Gaitan Prado", "doc": "6343469", "fecha": "09/02/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Blanca Yeneth Meneses", "doc": "29581881", "fecha": "01/01/1991", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "943", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble verificado con prioridad media.",
        "personas": [
            {"nombre": "Norma E. Bitega Prado", "doc": "76291089", "fecha": "14/02/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Marina Casamachin", "doc": "29972057", "fecha": "27/05/1994", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "944", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con muros y losas con riesgo de colapso, terreno asentado.",
        "personas": [
            {"nombre": "Edaaddstranaroo Semerel", "doc": "14976409", "fecha": "13/10/1951", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Marta Elena Segura Murcia", "doc": "31902906", "fecha": "05/05/1961", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Jose Fernando Segura Murcia", "doc": "16760682", "fecha": "12/03/1959", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "945", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras menores en mampostería y repello.",
        "personas": [
            {"nombre": "Silvio Calixto Castillo", "doc": "14955563", "fecha": "14/10/1948", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ofelia Calle", "doc": "31474760", "fecha": "17/11/1956", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "946", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con fisuras graves en mampostería y riesgo de colapso.",
        "personas": [
            {"nombre": "Manuma Setodilo Cernal", "doc": "6342125", "fecha": "22/11/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Jazmin Martinez S.", "doc": "1007632285", "fecha": "21/02/2002", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Rodrigo Hernan Velazco", "doc": "94429187", "fecha": "05/04/1975", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Juan Camilo Velazco", "doc": "1118307526", "fecha": "21/02/1996", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "947", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras en paredes y pisos.",
        "personas": [
            {"nombre": "Ibier Joel Cruz Quigua", "doc": "4664571", "fecha": "01/07/1976", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sandra Patricia Mona Nieto", "doc": "31485404", "fecha": "03/05/1980", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Mariana Cruz Mona", "doc": "1116377858", "fecha": "06/12/2013", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "948", "corregimiento": "Estancia Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con prioridad baja verificado.",
        "personas": [
            {"nombre": "Tatiana Moncaya Pinta", "doc": "1605785603", "fecha": "08/01/2003", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hiller", "doc": "1086332849", "fecha": "27/05/1999", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "949", "corregimiento": "Estancia Vieja", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con revisión completada sin novedad grave.",
        "personas": [
            {"nombre": "Victoria Percico", "doc": "31967992", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sebastian Acuña", "doc": "1005861183", "fecha": "18/01/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Cristian Prado", "doc": "16550987", "fecha": "11/08/1997", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "950", "corregimiento": "Estancia Vieja", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con fisuras en muros y acabados reportados.",
        "personas": [
            {"nombre": "Jaqueline Betancourt", "doc": "31485791", "fecha": "31/03/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andres Felipe Urrego Betancor", "doc": "1116383189", "fecha": "22/09/2020", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 931-950...")
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
        print(f"MIGRACIÓN LOTE 931-950 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
