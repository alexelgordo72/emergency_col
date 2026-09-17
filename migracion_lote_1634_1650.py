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
        "num_formulario": "1634", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Molieth Alexandra Muñoz - Prioridad media (RUFE-1634).",
        "personas": [
            {"nombre": "Molieth Alexandra Muñoz", "doc": "1118302341", "fecha": "23/04/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juan Sebastian Potosi", "doc": "1116375706", "fecha": "31/12/2010", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Anana Andrea Velazco", "doc": "1232833168", "fecha": "30/07/2024", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1635", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Carmen Emilia Gutierrez Loding - Vive sola, prioridad media (RUFE-1635).",
        "personas": [
            {"nombre": "Carmen Emilia Gutierrez Loding", "doc": "31901365", "fecha": "29/10/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1636", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Damaris Castaño Diaz - Prioridad media (RUFE-1636).",
        "personas": [
            {"nombre": "Damaris Castaño Diaz", "doc": "41908585", "fecha": "18/04/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Marco Aurelio Guerrero", "doc": "7546764", "fecha": "13/03/1965", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Marco Elias Guerrero", "doc": "1118287611", "fecha": "19/07/1988", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1637", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Maria Omaña Espinoza - Fisuras en juntas de muros divisorios y uno descolgado, prioridad media (RUFE-1637).",
        "personas": [
            {"nombre": "Maria Omaña Espinoza", "doc": "29811009", "fecha": "04/11/1952", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Midder Alberto Ballen", "doc": "1118304990", "fecha": "11/11/1995", "es_jefe": False, "sexo": "M", "parentesco": "Familiar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1638", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Luis Carlos Suarez - Prioridad baja (RUFE-1638).",
        "personas": [
            {"nombre": "Luis Carlos Suarez", "doc": "16667172", "fecha": "15/01/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1639", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Yeim Alexandra Calambis Montilla - Prioridad baja (RUFE-1639).",
        "personas": [
            {"nombre": "Yeim Alexandra Calambis Montilla", "doc": "1118298262", "fecha": "08/01/1991", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Daivo Martin Gomez", "doc": "0", "fecha": "12/06/2026", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1640", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Evelin Salazar - Prioridad baja (RUFE-1640).",
        "personas": [
            {"nombre": "Evelin Salazar", "doc": "1118306708", "fecha": "10/01/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Anunciación Luligo", "doc": "32540001", "fecha": "15/11/1984", "es_jefe": False, "sexo": "F", "parentesco": "Familiar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1641", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Sarbelio Muñoz - Prioridad baja (RUFE-1641).",
        "personas": [
            {"nombre": "Sarbelio Muñoz", "doc": "4668190", "fecha": "29/08/1967", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Zoraida Guacara Potosi", "doc": "25404467", "fecha": "25/04/1973", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1642", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Linda Isabela Payan Solarte - Prioridad baja (RUFE-1642).",
        "personas": [
            {"nombre": "Linda Isabela Payan Solarte", "doc": "1104924558", "fecha": "21/06/2006", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Isabel Melo Solarte", "doc": "1109939845", "fecha": "22/12/1993", "es_jefe": False, "sexo": "F", "parentesco": "Familiar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1643", "corregimiento": "Dionisio", "prioridad": "BAJA",
        "observaciones_evaluador": "Anna Marcela Lenis - Prioridad baja (RUFE-1643).",
        "personas": [
            {"nombre": "Anna Marcela Lenis", "doc": "1104843754", "fecha": "02/02/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Henrin Santiago Osorio", "doc": "11182933009", "fecha": "27/11/2021", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1644", "corregimiento": "Dionisio", "prioridad": "BAJA",
        "observaciones_evaluador": "Alba Fany Sanchez - Prioridad baja (RUFE-1644).",
        "personas": [
            {"nombre": "Alba Fany Sanchez", "doc": "29939858", "fecha": "08/01/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1645", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Margarita Maria Martinez Duke - Prioridad baja habitable (RUFE-1645).",
        "personas": [
            {"nombre": "Margarita Maria Martinez Duke", "doc": "1144058165", "fecha": "05/12/1992", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1646", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Daniela Jovecl Perez Jovel - Prioridad baja habitable (RUFE-1646).",
        "personas": [
            {"nombre": "Daniela Jovecl Perez Jovel", "doc": "11183045", "fecha": "20/04/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1647", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Jose Laiver Montenegro - Prioridad baja habitable (RUFE-1647).",
        "personas": [
            {"nombre": "Jose Laiver Montenegro", "doc": "1060868776", "fecha": "16/10/1986", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1648", "corregimiento": "Panorama Mirador", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jesica Liliana Puente - Prioridad media (RUFE-1648).",
        "personas": [
            {"nombre": "Jesica Liliana Puente", "doc": "68296084", "fecha": "19/11/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cristofer David Puente Enriquez", "doc": "1709187594", "fecha": "25/09/2006", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1649", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Leonardo Pava Lizcano - Edificación con problemas, paredes averiadas (RUFE-1649).",
        "personas": [
            {"nombre": "Leonardo Pava Lizcano", "doc": "79636992", "fecha": "04/03/1973", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Doris Martinez", "doc": "67012057", "fecha": "18/02/1978", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Joan Camilo Pava Martinez", "doc": "1019127971", "fecha": "02/12/1996", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1650", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Zandrea Jose Humeo Urbano - Prioridad media, no habitable (RUFE-1650).",
        "personas": [
            {"nombre": "Zandrea Jose Humeo Urbano", "doc": "94361692", "fecha": "16/07/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juan Diego Duque", "doc": "1117620796", "fecha": "19/05/2007", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1634-1650...")
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
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE documento_identidad = %s", (p["doc"],))
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
        print(f"MIGRACIÓN LOTE 1634-1650 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
