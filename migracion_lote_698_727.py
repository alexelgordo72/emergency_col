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
        "num_formulario": "698", "corregimiento": "Buenos Aires", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda prefabricada, con grandes dilataciones y asentamiento en muros. Riesgo para adultos mayores[cite: 73].",
        "personas": [
            {"nombre": "Nelly del Carmen Chauza", "doc": "31403657", "fecha": "13/07/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Bolivar Galeano Bravo", "doc": "6340334", "fecha": "12/07/1939", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Luz Maria Chaupa", "doc": "29982032", "fecha": "31/12/1935", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "699", "corregimiento": "Arroyohondo", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras superficiales, sin afectaciones graves. Habitable[cite: 73].",
        "personas": [
            {"nombre": "Yeny Rivera Garcia", "doc": "34615162", "fecha": "31/08/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Edilberto Armero Guillota", "doc": "3206109197", "fecha": "20/12/1975", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Diego Fernando Santacruz Rivera", "doc": "1062277845", "fecha": "21/10/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "700", "corregimiento": "Trinidad", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con cielo raso colapsado y cubierta rodada, sin afectaciones mayores[cite: 73].",
        "personas": [
            {"nombre": "Juliana Murillo Moreno", "doc": "1118306979", "fecha": "30/06/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Monica Becerra", "doc": "31480680", "fecha": "08/05/1976", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "713", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con dilatación de paredes[cite: 74].",
        "personas": [
            {"nombre": "Gustavo Adolfo Chilito Cordoba", "doc": "1118758014", "fecha": "25/03/1991", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cielo Maria Pismac Garcia", "doc": "1006850547", "fecha": "22/12/2002", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "714", "corregimiento": "Bolívar", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con dilatación en las paredes[cite: 74].",
        "personas": [
            {"nombre": "Orfilia Echeverry Valencia", "doc": "29971888", "fecha": "04/12/1945", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "720", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras en mampostería[cite: 75].",
        "personas": [
            {"nombre": "Tulio Marino Rodriguez", "doc": "6547771", "fecha": "27/04/1943", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "721", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras superficiales en muros y conexión de viga y muro[cite: 75].",
        "personas": [
            {"nombre": "Nelson Montenegro", "doc": "16457956", "fecha": "03/10/1978", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Faisory Salas Vidal", "doc": "1118290545", "fecha": "17/07/1988", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Yeshuan Reina Salas", "doc": "1232819163", "fecha": "19/07/2013", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "722", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble evaluado con fisuras mínimas, habitable[cite: 75].",
        "personas": [
            {"nombre": "Fenix Nieva Martinez", "doc": "31465737", "fecha": "06/08/1956", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "723", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble evaluado tras sismo, sin daños mayores estructurales.",
        "personas": [
            {"nombre": "Maria Pricily Olarte", "doc": "1118288736", "fecha": "08/06/1988", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Aura Maria Campo Olarte", "doc": "318763329", "fecha": "09/08/1947", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Martha Oliva Olarte", "doc": "314694817", "fecha": "11/11/1962", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Alison Sanchez Campo", "doc": "1118312486", "fecha": "03/06/2018", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "724", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 2 pisos con fisuras en muros de mampostería y soportes[cite: 76].",
        "personas": [
            {"nombre": "Leid Johana Gaviria", "doc": "1118303888", "fecha": "01/01/1997", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jofia Flover Garcia", "doc": "1118302197", "fecha": "13/01/1969", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Patricia Rengifo Alive C.", "doc": "29939915", "fecha": "30/09/1988", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Edwin Gaviria R.", "doc": "1118289962", "fecha": "30/10/2008", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Samuel Gaviria", "doc": "1107854274", "fecha": "27/02/2020", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "725", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con grietas superficiales en paredes de adobe[cite: 76].",
        "personas": [
            {"nombre": "Henry Cano Aguirre", "doc": "10174034", "fecha": "04/06/1968", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "726", "corregimiento": "Las Vegas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado con propietario ocasional[cite: 76].",
        "personas": [
            {"nombre": "Arcer Polanco", "doc": "1648133", "fecha": "06/01/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "727", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con agrietamientos superficiales en la fachada[cite: 76].",
        "personas": [
            {"nombre": "Juan Carlos Salcedo Murcia", "doc": "16737870", "fecha": "28/03/1967", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria del Pilar Sanchez Holguin", "doc": "66770199", "fecha": "28/11/1973", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Juan Camilo Salcedo Sanchez", "doc": "1118311870", "fecha": "17/09/1998", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 698-727...")
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
        print(f"MIGRACIÓN LOTE 698-727 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
