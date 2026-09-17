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
        "num_formulario": "236", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bareque colapsada sin cimientos.",
        "personas": [
            {"nombre": "Otilia Astudillo", "doc": "48602121", "fecha": "23/05/1961", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Isidora Alvarez", "doc": "29975798", "fecha": "06/10/1959", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "237", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda inhabitable con riesgo de colapso inminente, sistema estructural dilatado, mampostería comprometida 80%.",
        "personas": [
            {"nombre": "Luz Marina Posada", "doc": "29975202", "fecha": "18/06/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diana Marcela Prado", "doc": "1144159162", "fecha": "10/07/1992", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Elmer Jhonson Buitrago", "doc": "1144157313", "fecha": "08/05/1992", "es_jefe": False, "sexo": "M", "parentesco": "Yerno", "etnia": "Ninguna"},
            {"nombre": "Juan Martin Buitrago", "doc": "1116380679", "fecha": "14/04/2017", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "238", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda no habitable por posible colapso, columnas y vigas en madera. Presenta agrietamiento.",
        "personas": [
            {"nombre": "Carlos Enrique Posada", "doc": "16559022", "fecha": "23/08/1958", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Dary Rivera", "doc": "29872625", "fecha": "29/12/1969", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "239", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Parcialmente derrumbada, deficiencia en cimentación, derrumbe en mampostería 70% y cubierta.",
        "personas": [
            {"nombre": "Laurentina Joaqui", "doc": "25641127", "fecha": "12/02/1935", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alcibar Hoyos", "doc": "94185001", "fecha": "26/10/1958", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Lizeth Vanessa Hoyos", "doc": "1118301756", "fecha": "14/12/1993", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Yoselin Ordoñez", "doc": "1232797076", "fecha": "24/05/2016", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Jefferson Hoyos", "doc": "1118296403", "fecha": "20/07/1991", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "240", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Alta probabilidad de colapso en techo y muros. Estructura en guadua comprometida.",
        "personas": [
            {"nombre": "Monica Salazar", "doc": "52255557", "fecha": "20/05/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jimena Galindo", "doc": "0", "fecha": "28/12/1973", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "241", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda sin estructura definida, en posible colapso. Asentamiento con desplazamiento.",
        "personas": [
            {"nombre": "Julian Otoya", "doc": "14956114", "fecha": "13/06/1949", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "242", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda prefabricada colapsada e inhabitable.",
        "personas": [
            {"nombre": "Jhon Ever Tamayo", "doc": "1060108198", "fecha": "14/06/1997", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "243", "corregimiento": "Buitrera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mampostería afectada, columna fisurada.",
        "personas": [
            {"nombre": "Hugo Piamba", "doc": "16453859", "fecha": "09/01/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cristhian Fernandez", "doc": "1118297860", "fecha": "14/03/1992", "es_jefe": False, "sexo": "M", "parentesco": "Yerno", "etnia": "Ninguna"},
            {"nombre": "Yessica Piamba", "doc": "1118309201", "fecha": "19/12/1997", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Rosalba Fernandez", "doc": "31971444", "fecha": "22/11/1968", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Nolver Noguera", "doc": "1118290058", "fecha": "17/12/1987", "es_jefe": False, "sexo": "M", "parentesco": "Yerno", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "245", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mampostería comprometida 75%. Obra blanca destruida 80%.",
        "personas": [
            {"nombre": "Hector Cabezas", "doc": "94401936", "fecha": "18/09/1974", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hilary Cabezas", "doc": "1144207462", "fecha": "12/10/1989", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Sandra Cabezas", "doc": "38886547", "fecha": "14/04/1973", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "246", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Estructura averiada en juntas de columnas y vigas. Mampostería afectada 50%.",
        "personas": [
            {"nombre": "Nubia Rojas", "doc": "25453741", "fecha": "06/07/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "248", "corregimiento": "Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Mampostería afectada 90%. Sistema Estructural en Madera Averiado.",
        "personas": [
            {"nombre": "Cecilia Battle", "doc": "29074692", "fecha": "24/03/1961", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gustavo Zamorano", "doc": "16448050", "fecha": "01/08/1957", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "249", "corregimiento": "Buitrera", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras en todo el sistema estructural y desplazamiento en el terreno.",
        "personas": [
            {"nombre": "Santo Egred", "doc": "16659454", "fecha": "09/09/1955", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Daniela Mosquera", "doc": "5068198", "fecha": "14/05/2001", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "251", "corregimiento": "Buitrera", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda habitable, con fisuras transversales y longitudinales Leves en mampostería.",
        "personas": [
            {"nombre": "Vladimir Correa", "doc": "94491837", "fecha": "14/09/1976", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yohanna Arcila", "doc": "31484762", "fecha": "14/03/1971", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    }
]

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match:
        return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO (Upsert) Lote 236-253 (Corregido)...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        formularios_creados, formularios_actualizados = 0, 0
        personas_creadas, personas_actualizadas = 0, 0
        
        for form in LOTES_NUEVOS_RUFE:
            num_limpio = form["num_formulario"].lstrip('0')
            
            cur.execute("SELECT id FROM public.rufe_formularios WHERE numero_formulario = %s", (num_limpio,))
            resultado = cur.fetchone()
            
            if resultado:
                form_id = resultado[0]
                cur.execute("""
                    UPDATE public.rufe_formularios 
                    SET prioridad = %s, observaciones_evaluador = %s
                    WHERE id = %s;
                """, (form["prioridad"], form["observaciones_evaluador"], form_id))
                formularios_actualizados += 1
            else:
                cur.execute("""
                    INSERT INTO public.rufe_formularios 
                    (reporte_id, numero_formulario, corregimiento, prioridad, observaciones_evaluador)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id;
                """, (str(uuid.uuid4()), num_limpio, form["corregimiento"], form["prioridad"], form["observaciones_evaluador"]))
                form_id = cur.fetchone()[0]
                formularios_creados += 1
                
            for p in form["personas"]:
                if p["doc"] == "0": continue
                edad_calc = calcular_edad_2026(p["fecha"])
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE REPLACE(documento_identidad, '.', '') = %s", (p["doc"],))
                res_persona = cur.fetchone()
                
                if res_persona:
                    persona_id = res_persona[0]
                    cur.execute("""
                        UPDATE public.rufe_personas 
                        SET fecha_nacimiento = %s, edad = %s, es_jefe_hogar = %s, parentesco = %s, sexo = %s, etnia = %s
                        WHERE id = %s;
                    """, (p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], persona_id))
                    personas_actualizadas += 1
                else:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, edad, es_jefe_hogar, parentesco, sexo, etnia)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (form_id, p["nombre"], p["doc"], p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"]))
                    personas_creadas += 1

        print(f"\n==================================================")
        print(f"MIGRACIÓN LOTE 236-253 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
