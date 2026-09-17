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
    # --- EL LOTE OMITIDO (451-460) ---
    {
        "num_formulario": "451", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda prefabricada con fisuras en muros de mampostería, muros de la cocina. Habitable.",
        "personas": [
            {"nombre": "Luis Carlos Loaiza Garcia", "doc": "1118295539", "fecha": "29/03/1988", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Leidy Yolanda Salas", "doc": "31485385", "fecha": "02/09/1982", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "452", "corregimiento": "La Cumbre", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque colapsada. Inhabitable. Ubicación de la cumbre en muy mala condición.",
        "personas": [
            {"nombre": "Maria Edubina Urbano Romero", "doc": "39840657", "fecha": "22/08/1971", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Olga Lucia Urbano", "doc": "1118304413", "fecha": "16/10/1993", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "453", "corregimiento": "Montañitas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda prefabricada. Se soltaron modulos de plaquetas que ya fueron organizadas. Riesgo bajo habitable.",
        "personas": [
            {"nombre": "Juan Carlos Perez", "doc": "16642793", "fecha": "02/07/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "454", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en 3 componentes: 1. Bahareque (50% colapsada), 2. Farol (20% habitable), 3. Madera (20% habitable). Medianamente habitable.",
        "personas": [
            {"nombre": "Nidia Maria Ramirez", "doc": "29583427", "fecha": "10/12/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Daladier Antonio Ramirez", "doc": "14577114", "fecha": "06/04/1992", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jose Manuel Anaya Jurado", "doc": "1232797076", "fecha": "04/05/2016", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Andres Felipe Muñoz", "doc": "1118305886", "fecha": "20/07/1991", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "455", "corregimiento": "Montañitas", "prioridad": "BAJA",
        "observaciones_evaluador": "Fallo cubierta de techo en la cocina. El resto es habitable.",
        "personas": [
            {"nombre": "Rosa Maria Herrera", "doc": "31469042", "fecha": "18/01/1963", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Elsa Nubia Imbachi", "doc": "29975350", "fecha": "04/12/1984", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "456", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Hay persona con discapacidad. Vivienda sin sistema estructural construida en mampostería. Fisuras aparentemente superficiales.",
        "personas": [
            {"nombre": "Deyfa Tello", "doc": "29105495", "fecha": "11/05/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Duberney Bernal", "doc": "94320315", "fecha": "10/07/1974", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Ignacio Andres Tello", "doc": "1107055260", "fecha": "24/04/1989", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "457", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Caseta comunal Filo Laguna.",
        "personas": [
            {"nombre": "Adriana Rosero", "doc": "66814602", "fecha": "21/04/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "458", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda prefabricada con daños y reparaciones locativas y una fisura en losa parte posterior. Riesgo de deslizamiento.",
        "personas": [
            {"nombre": "Cindy Rodriguez", "doc": "1151935865", "fecha": "04/08/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Kevin Andres Montesdeoca", "doc": "1151960689", "fecha": "06/11/1996", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Miguel Angel Burbano", "doc": "1109547297", "fecha": "22/12/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "459", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda colapsada.",
        "personas": [
            {"nombre": "Alexander Bejarano", "doc": "167595272", "fecha": "16/01/1971", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sandra Ibarguen", "doc": "66998415", "fecha": "08/03/1977", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Brandon Bejarano", "doc": "1116180186", "fecha": "18/03/2011", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "460", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda destruida.",
        "personas": [
            {"nombre": "Alexa Bejarano", "doc": "1007734703", "fecha": "06/05/2001", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hilary Bejarano", "doc": "1109121010", "fecha": "22/01/2020", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    # --- LOS DEL 461 AL 468 (Ya parseados, incluidos para completar UPSERT) ---
    {
        "num_formulario": "461", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda sin sistema estructural construida en mampostería. Fisuras aparentemente superficiales.",
        "personas": [
            {"nombre": "Deyfa Tello", "doc": "29105495", "fecha": "11/05/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Duberney Bernal", "doc": "94320315", "fecha": "10/07/1974", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Ignacio Andres Tello", "doc": "1107055260", "fecha": "24/04/1989", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "462", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque a punto de caer. Colapsada sin ningún tipo de estructura.",
        "personas": [
            {"nombre": "Lisandro Paladines", "doc": "16539315", "fecha": "16/12/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Angel Ochoa", "doc": "27205362", "fecha": "11/05/1998", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Gerson Jesus Diaz Ochoa", "doc": "107667193", "fecha": "16/05/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Gerardo Josue Diaz Ochoa", "doc": "107667221", "fecha": "17/06/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Disleidy Carolina Escalona", "doc": "35009164", "fecha": "18/02/2007", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Surley Paladines", "doc": "16454516", "fecha": "17/12/1973", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "463", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Casa en bahareque habitable con 3 muros comprometidos en la zona de la cocina.",
        "personas": [
            {"nombre": "Gentil Ordoñez", "doc": "4707967", "fecha": "03/03/1952", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Rosanefi Benavidez", "doc": "34445029", "fecha": "12/06/1964", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Mauro Gentil Ordoñez", "doc": "1118288824", "fecha": "16/12/1987", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "464", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda estructuralmente ineficiente. Se recomienda realizar reforzamiento.",
        "personas": [
            {"nombre": "Pablo Burgos", "doc": "13249844", "fecha": "01/12/1952", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Erlyn Yudith Burgos", "doc": "38610198", "fecha": "05/11/1981", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Jhoan David Burgos", "doc": "1118302889", "fecha": "16/07/2012", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jorge Andres Burgos", "doc": "1006033614", "fecha": "31/10/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "465", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en tablas con parte de estructura de madera y desplazamiento de masa de tierra en la parte posterior.",
        "personas": [
            {"nombre": "Ivan Delgado", "doc": "5351625", "fecha": "02/07/1948", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Oscar Delgado", "doc": "16588337", "fecha": "18/09/1954", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "466", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en madera con algunas averías. Requieren reparaciones parciales.",
        "personas": [
            {"nombre": "Amparo Reyes", "doc": "38855013", "fecha": "19/03/1951", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Dano Villamil", "doc": "14994964", "fecha": "01/10/1952", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Katerin Villamil", "doc": "1106513721", "fecha": "10/11/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jacobo Villamil", "doc": "1110000000", "fecha": "20/01/2022", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "467", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con sistema estructural averiado en la parte posterior y mampostería debilitada. Inminente colapso.",
        "personas": [
            {"nombre": "Maria Alicia Caicedo", "doc": "31258883", "fecha": "30/11/1949", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Libardo Rivera", "doc": "4952561", "fecha": "29/07/1960", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Aixa Rivera", "doc": "1105361921", "fecha": "14/09/2004", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "468", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en mampostería.",
        "personas": [
            {"nombre": "Yamileth Cardona", "doc": "31582594", "fecha": "22/08/1979", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Wilfrank Cardenas", "doc": "94509035", "fecha": "02/10/1977", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Jaider Cardenas", "doc": "1108334776", "fecha": "03/09/2002", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ana Sofia Cardenas", "doc": "1116000000", "fecha": "26/09/2006", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL (Lote 451-468 completo)...")
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
        print(f"MIGRACIÓN FINAL LOTE 451-468 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
