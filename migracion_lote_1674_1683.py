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
        "num_formulario": "1674", "corregimiento": "Currao", "prioridad": "ALTA",
        "observaciones_evaluador": "Walter Tigreros Molina - Edificio con apartamentos mixtos (algunos prioritarios no habitables y otros habitables) (RUFE-1674)[cite: 40].",
        "personas": [
            {"nombre": "Walter Tigreros Molina", "doc": "16636150", "fecha": "17/04/1960", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Alberto Tigreros", "doc": "1182013705", "fecha": "06/08/1983", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Carolina Molina Vergara", "doc": "111642472", "fecha": "27/09/1991", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1675", "corregimiento": "Panorama", "prioridad": "ALTA",
        "observaciones_evaluador": "Iris Casquete - Caso de embarazo, prioridad alta (RUFE-1675)[cite: 40].",
        "personas": [
            {"nombre": "Iris Casquete", "doc": "1192754462", "fecha": "08/05/1991", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nefer Jon Renteria Casquete", "doc": "1111829988", "fecha": "19/05/2009", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1676", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Herminia Trujillo Lopez - Vivienda no habitable por daños severos (RUFE-1676)[cite: 40].",
        "personas": [
            {"nombre": "Herminia Trujillo Lopez", "doc": "66933424", "fecha": "16/07/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luciana Martinez Trujillo", "doc": "1116380961", "fecha": "30/07/2017", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1677", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Nolida Fajardo Salinas - Finca Las Palmas, no habitable (RUFE-1677)[cite: 41].",
        "personas": [
            {"nombre": "Nolida Fajardo Salinas", "doc": "345057788", "fecha": "09/01/1943", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Pedro Pablo Salinas", "doc": "6743494", "fecha": "29/06/1943", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1678", "corregimiento": "San Marcos", "prioridad": "ALTA",
        "observaciones_evaluador": "Degakorto Garcia Mosquera - Vivienda rural no habitable (RUFE-1678)[cite: 41].",
        "personas": [
            {"nombre": "Degakorto Garcia Mosquera", "doc": "14932485", "fecha": "23/01/1946", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Gloria Ines Mosquera", "doc": "25329082", "fecha": "07/09/1977", "es_jefe": False, "sexo": "F", "parentesco": "Familiar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1679", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Edwin Ferney Monzuno Matta - Fisuras en muros, corrosión en acero de columnas y losa de entrepiso (RUFE-1679)[cite: 41].",
        "personas": [
            {"nombre": "Edwin Ferney Monzuno Matta", "doc": "1144731836", "fecha": "06/07/1989", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Claudia Jimena Escobar Muñoz", "doc": "1118291916", "fecha": "07/07/1992", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1680", "corregimiento": "San Jorge", "prioridad": "MEDIA",
        "observaciones_evaluador": "Laimaria Serna - Trono de Azúcar, prioridad media (RUFE-1680)[cite: 41].",
        "personas": [
            {"nombre": "Laimaria Serna", "doc": "1118305398", "fecha": "20/10/2000", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1681", "corregimiento": "Panorama", "prioridad": "MEDIA",
        "observaciones_evaluador": "Gloria Ortega - Prioridad media (RUFE-1681)[cite: 41].",
        "personas": [
            {"nombre": "Gloria Ortega", "doc": "29401150", "fecha": "01/01/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1682", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Martha Ines Rubio Galeano - Deterioro severo con acero expuesto y corrosión en placa-losa (RUFE-1682)[cite: 41].",
        "personas": [
            {"nombre": "Martha Ines Rubio Galeano", "doc": "66922758", "fecha": "05/01/1974", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alexander Cardona", "doc": "6549717", "fecha": "15/03/1985", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Monica Andrea Batero Rubio", "doc": "1151945172", "fecha": "06/02/1992", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1683", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jovicy Cristina Morales Moncayo - Prioridad media habitable (RUFE-1683)[cite: 41].",
        "personas": [
            {"nombre": "Jovicy Cristina Morales Moncayo", "doc": "94379197", "fecha": "17/04/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Santiago Martinez", "doc": "1144097927", "fecha": "04/08/1997", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1674-1683...")
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
        print(f"MIGRACIÓN LOTE 1674-1683 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
