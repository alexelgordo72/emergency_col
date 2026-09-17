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
        "num_formulario": "417", "corregimiento": "Belalcazar", "prioridad": "ALTA",
        "observaciones_evaluador": "Riesgo Medio Alto por posible caída de techo en la cocina (cubierta en esterilla).",
        "personas": [
            {"nombre": "Jose Ignacio Poca Neira", "doc": "16735427", "fecha": "23/09/1954", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "418", "corregimiento": "Gaitan", "prioridad": "MEDIA",
        "observaciones_evaluador": "Separación y fisura localizada en la parte inferior de la cubierta. Grietas leves.",
        "personas": [
            {"nombre": "Ana Racheli Cambero", "doc": "6082843", "fecha": "15/02/1988", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Willin Carmona", "doc": "6065498", "fecha": "02/12/1984", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "419", "corregimiento": "Las Cruces", "prioridad": "MEDIA",
        "observaciones_evaluador": "Riesgo medio por cielo raso suelto sobre área de circulación de niños.",
        "personas": [
            {"nombre": "Sandra Neira Cortes", "doc": "66987696", "fecha": "22/11/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hoover Agudelo Alegria", "doc": "1118307858", "fecha": "14/03/1990", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "420", "corregimiento": "Las Cruces", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en pañete. Se consideran fisuras estéticas.",
        "personas": [
            {"nombre": "Leonardo Correa", "doc": "1118303416", "fecha": "24/10/1994", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "421", "corregimiento": "Las Cruces", "prioridad": "BAJA",
        "observaciones_evaluador": "Sin novedad.",
        "personas": [
            {"nombre": "Victor Guzman", "doc": "14670028", "fecha": "31/08/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "422", "corregimiento": "Panoramica", "prioridad": "BAJA",
        "observaciones_evaluador": "Se presentan fisuras superficiales en pañete. Fisura en el archivo.",
        "personas": [
            {"nombre": "Anderson Molina", "doc": "1144187136", "fecha": "11/04/1996", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "423", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Fracturas en la columna que debe ser retirada. Desprendimiento de muro en cocina.",
        "personas": [
            {"nombre": "Geronimo Velazquez", "doc": "5999668", "fecha": "08/08/1988", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "424", "corregimiento": "El Silencio", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con desplome de muros divisorios de mampostería. Inhabitable con riesgo latente.",
        "personas": [
            {"nombre": "Nora Chicangana", "doc": "106692285", "fecha": "15/01/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "425", "corregimiento": "El Rosal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque colapsada en un 80%.",
        "personas": [
            {"nombre": "Maria Lucy Giraldo Jaramillo", "doc": "66712679", "fecha": "21/03/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alfredo Zuñiga Mera", "doc": "16448300", "fecha": "01/03/1968", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "426", "corregimiento": "Uribe", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque con desprendimiento de material en muros y cubierta inestable. Inhabitable.",
        "personas": [
            {"nombre": "Ana Lucia Rengifo", "doc": "38992373", "fecha": "05/05/1948", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gustavo Rengifo", "doc": "16581581", "fecha": "24/07/1970", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "427", "corregimiento": "Bolivar", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en pañete. Se recomienda hacer revoque.",
        "personas": [
            {"nombre": "Valentino Gañan Vargas", "doc": "1147615653", "fecha": "30/04/1999", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Belarmina Vargas", "doc": "66814125", "fecha": "21/08/1959", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "428", "corregimiento": "Zamoranos", "prioridad": "BAJA",
        "observaciones_evaluador": "Mampostería afectada 90%. Sistema Estructural en Madera Averiado.",
        "personas": [
            {"nombre": "Cecilia Elena Battle", "doc": "29074692", "fecha": "24/03/1961", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gustavo Zamorano", "doc": "16448050", "fecha": "01/08/1957", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "429", "corregimiento": "Buitrera", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras en todo el sistema estructural y desplazamiento.",
        "personas": [
            {"nombre": "Santo Ricardo Egred", "doc": "16659454", "fecha": "09/09/1955", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Daniela Mosquera", "doc": "5068198", "fecha": "14/05/2001", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "430", "corregimiento": "Centro", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisura en sistema estructural entre columna.",
        "personas": [
            {"nombre": "Maria Eugenia Lozano", "doc": "31470858", "fecha": "27/10/1963", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    }
]

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match:
        return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO Lote COMPLETO 417-430...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
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
                    SET prioridad = %s, observaciones_evaluador = %s
                    WHERE id = %s;
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
        print(f"MIGRACIÓN LOTE 417-430 (COMPLETO) EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
