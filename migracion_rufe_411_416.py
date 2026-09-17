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

LOTE_FINAL_RUFE = [
    {
        "num_formulario": "411", "corregimiento": "Nuevo Horizonte", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque fuertemente agrietada, se recomienda desalojo por peligro inminente de caída.",
        "personas": [
            {"nombre": "Cesar Mondragon", "doc": "1118288534", "fecha": "31/05/1991", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Stiven Mondragon", "doc": "1118295930", "fecha": "09/04/1988", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "412", "corregimiento": "Trinidad", "prioridad": "MEDIA",
        "observaciones_evaluador": "Colapso parcial por falta de vigas de confinamiento y amarre. Fisura horizontal en 2do piso.",
        "personas": [
            {"nombre": "Francia de Jesus Guayara", "doc": "31468665", "fecha": "08/08/1988", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Darwin Steven Flores Guayara", "doc": "1125232015", "fecha": "19/08/1990", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Yurin Yesenia Yusty Guayara", "doc": "1118294556", "fecha": "11/09/2015", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Sheril Karina Chaverra Yusty", "doc": "1116379313", "fecha": "22/06/2017", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Manuel Andres Sanchez Yusty", "doc": "1116383775", "fecha": "01/01/2019", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "413", "corregimiento": "Buenos Aires", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda sin vigas de amarre. Muros sueltos. Techo y remates de columnas colapsados. Escaleras con acero expuesto.",
        "personas": [
            {"nombre": "Jhon Jairo Ipiales", "doc": "16462204", "fecha": "21/03/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Consuelo Meneses", "doc": "1118256922", "fecha": "01/06/1987", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Daylin Ipiales", "doc": "1005967245", "fecha": "14/05/2010", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "414", "corregimiento": "Buenos Aires", "prioridad": "ALTA",
        "observaciones_evaluador": "Materiales reciclados (madera, esterilla, zinc) en muy mal estado. Al borde de un talud con riesgo de deslizamiento. Madre e hijo con problemas psiquiátricos.",
        "personas": [
            {"nombre": "Maria Amanda Meneses", "doc": "31483135", "fecha": "21/09/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Deiby Antonio Meneses", "doc": "1118310581", "fecha": "16/11/1996", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "415", "corregimiento": "Nuevo Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muro suelto en fachada de 2do piso por falta de columnas. Suelta baranda 2 piso. Falta dintel en primer piso.",
        "personas": [
            {"nombre": "Karina Paredes", "doc": "31580778", "fecha": "05/10/1979", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Arcelio Fonseca", "doc": "94071070", "fecha": "04/04/1976", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "416", "corregimiento": "Nuevo Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Losa apoyada en bahareque y madera. Se recomienda demoler losa por peso y reforzar pilares.",
        "personas": [
            {"nombre": "Ana Maria Henao", "doc": "31144118", "fecha": "26/01/1952", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sorfi Junot Chavarriaga", "doc": "66757741", "fecha": "26/03/1969", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Sandra Patricia Henao", "doc": "66761096", "fecha": "17/10/1970", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Yeral Valentina Henao", "doc": "1191219221", "fecha": "05/10/2013", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Beatriz Bermudez", "doc": "31477813", "fecha": "11/04/1974", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    }
]

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match:
        return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO (Upsert) Lote 411-416...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        formularios_creados, formularios_actualizados = 0, 0
        personas_creadas, personas_actualizadas = 0, 0
        
        for form in LOTE_FINAL_RUFE:
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
        print(f"MIGRACIÓN LOTE 411-416 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
