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
        "num_formulario": "676", "corregimiento": "Hacienda Verde", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en mampostería, se recomienda demoler muro de la habitación por riesgo.",
        "personas": [
            {"nombre": "Fabiola Lopez", "doc": "31478533", "fecha": "30/01/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "677", "corregimiento": "La Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 1 piso en ladrillo sin confinamiento; fisuras en paredes y posible asentamiento de vigas[cite: 69].",
        "personas": [
            {"nombre": "Ana Lucia Rios Rico", "doc": "66702332", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Humberto Rico", "doc": "0", "fecha": "01/01/1965", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Juan Jose Arciniegas", "doc": "0", "fecha": "01/01/2005", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "678", "corregimiento": "La Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 2 pisos con fisuras transversales y asentamiento diferencial[cite: 69].",
        "personas": [
            {"nombre": "Luis Fernando Ordoñez", "doc": "16729163", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Esther Cecilia Vallejo", "doc": "3147829", "fecha": "01/01/1975", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Maria Camila Ordoñez", "doc": "1005868288", "fecha": "01/01/2000", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jeronimo Ordoñez", "doc": "1108257855", "fecha": "19/12/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "679", "corregimiento": "La Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en material con muros portantes y de cerramiento con riesgo alto de colapso[cite: 69].",
        "personas": [
            {"nombre": "Lida F. Quiñonez", "doc": "1118293850", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "680", "corregimiento": "La Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda antigua con techo en teja de barro y cielo raso deteriorado[cite: 69].",
        "personas": [
            {"nombre": "Yolanda Hincapie P.", "doc": "31906176", "fecha": "20/05/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Fernando Muñoz", "doc": "16661821", "fecha": "19/10/1959", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Victoria Bermudez", "doc": "0", "fecha": "01/01/1990", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "681", "corregimiento": "La Estancia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 1 piso con mampostería afectada y fisuras en muros.",
        "personas": [
            {"nombre": "Francisco Salazar", "doc": "14576614", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Oscar Salazar", "doc": "29581649", "fecha": "01/01/1975", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Fernando Salazar", "doc": "0", "fecha": "01/01/1980", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Laura Sofia Chaparro Reyes", "doc": "1192724552", "fecha": "09/09/2000", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jonathan Salazar", "doc": "31480341", "fecha": "27/08/2024", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "682", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 1 piso con parte delantera afectada por muros agrietados; se recomienda reforzar estructuralmente con columnas y vigas[cite: 69].",
        "personas": [
            {"nombre": "Victor Manuel Renteña Ospina", "doc": "11850552", "fecha": "10/03/1967", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Felipe Jaimes Ospina", "doc": "11850411", "fecha": "16/06/1954", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "683", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras menores en muros y separación entre la viga y el muro[cite: 69].",
        "personas": [
            {"nombre": "Cristian Ortiz", "doc": "1118300557", "fecha": "01/06/1993", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "684", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Edificio imponente con fisuras leves[cite: 69].",
        "personas": [
            {"nombre": "Frank Sebastián Quintero", "doc": "1151963370", "fecha": "22/10/1997", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "685", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de dos pisos con fisuras intermitentes en muros y columnas, y desprendimiento de revestimiento[cite: 69].",
        "personas": [
            {"nombre": "Hector Fabio Espinoza", "doc": "16663169", "fecha": "28/11/1978", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jorge Enrique Espinoza", "doc": "16679033", "fecha": "21/06/1981", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Carlos Enrique Espinoza", "doc": "1112483354", "fecha": "01/01/1990", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ana Lucia Urbina", "doc": "27488110", "fecha": "01/01/1975", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "686", "corregimiento": "Parques del Pinar", "prioridad": "BAJA",
        "observaciones_evaluador": "Apartamento con fisuras superficiales no estructurales[cite: 70].",
        "personas": [
            {"nombre": "Andres F. Menesses", "doc": "1061767021", "fecha": "14/02/1994", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "687", "corregimiento": "Parques del Pinar", "prioridad": "BAJA",
        "observaciones_evaluador": "Apartamento (Piso 8) con fisuras superficiales y separaciones menores[cite: 70].",
        "personas": [
            {"nombre": "Andres F. Menesses", "doc": "1061767021", "fecha": "14/02/1994", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "688", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de 3 pisos con concreto y mampostería, con fisuras y desprendimiento de repello en muros de fachada[cite: 70].",
        "personas": [
            {"nombre": "Valery Sanchez", "doc": "1116373868", "fecha": "20/04/2007", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Martin Ozuna Berdugo", "doc": "1119185161", "fecha": "03/05/2010", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Maria del Mar Ozuna Sanchez", "doc": "1109922443", "fecha": "22/03/2016", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 676-688...")
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
        print(f"MIGRACIÓN LOTE 676-688 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
