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
        "num_formulario": "621", "corregimiento": "Lucas", "prioridad": "ALTA",
        "observaciones_evaluador": "Cubierta en mal estado y fisuras en muros. Riesgo alto, no habitable[cite: 55].",
        "personas": [
            {"nombre": "Marleny Rodriguez Paya", "doc": "31466333", "fecha": "01/01/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Aracelly Paya Rodriguez", "doc": "38998532", "fecha": "01/01/1985", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Orlando Paya Rodriguez", "doc": "16452306", "fecha": "01/01/1980", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "622", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Pequeñas fisuras en muros, pérdida de repello en columna interior y daño leve en columna de fachada[cite: 56]. Riesgo bajo[cite: 56].",
        "personas": [
            {"nombre": "Hector Fabio Jordan Bernal", "doc": "149838255", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "623", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisura superficial en muro, sin hierro expuesto y viga superior del primer piso en buen estado. Habitable[cite: 57].",
        "personas": [
            {"nombre": "Enrique Quintero Diaz", "doc": "94360931", "fecha": "01/01/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Zoraida Quintero", "doc": "66993414", "fecha": "01/01/1970", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "624", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Vigas con desprendimiento de repello y separación de muros. Riesgo bajo.",
        "personas": [
            {"nombre": "Norbelly Narvaez", "doc": "231476597", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Elcy Narvaez", "doc": "331465777", "fecha": "01/01/1985", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "625", "corregimiento": "Campestre Real", "prioridad": "MEDIA",
        "observaciones_evaluador": "Afectación de fachadas, repellos y fisuras en muros no estructurales.",
        "personas": [
            {"nombre": "Maria Camila Varela", "doc": "1144704240", "fecha": "01/01/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "626", "corregimiento": "Bellavista", "prioridad": "ALTA",
        "observaciones_evaluador": "Asentamiento de piso construido sobre relleno mal compactado, con inminente riesgo de afectación a la vivienda[cite: 56].",
        "personas": [
            {"nombre": "Caroll Emilsen Garcia Bolaños", "doc": "7122337382", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Lina Marcela Salazar", "doc": "1113302355", "fecha": "01/01/1992", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "627", "corregimiento": "Bellavista", "prioridad": "MEDIA",
        "observaciones_evaluador": "Estructura en buen estado, pero con construcción vecina aledaña con elementos de soporte mal rellenados que podrían generar afectaciones[cite: 56].",
        "personas": [
            {"nombre": "Luis Alfonso Lopez", "doc": "16340139", "fecha": "13/12/1956", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Celia Morales de Lopez", "doc": "38710034", "fecha": "29/07/1960", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "628", "corregimiento": "Campestre Real", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras en muros y en repellos de la fachada. Riesgo bajo.",
        "personas": [
            {"nombre": "William Vallejo Gomez", "doc": "6253683", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "629", "corregimiento": "Bellavista", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en muros por desplazamiento, desprendimiento de estuco y repello en fachada del segundo piso[cite: 57].",
        "personas": [
            {"nombre": "Angel Luciano Astaiza", "doc": "16446569", "fecha": "23/04/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cristian Andres Astaiza", "doc": "111828551", "fecha": "05/01/1992", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "630", "corregimiento": "Bellavista", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en mampostería y acabados. Riesgo bajo[cite: 58].",
        "personas": [
            {"nombre": "Nataly Garcia", "doc": "1118299257", "fecha": "06/12/1998", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Marta Lucia Garcia", "doc": "31477074", "fecha": "17/05/1976", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "631", "corregimiento": "Buitrera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Daños estructurales menores en la unión columna-viga superior. Fisuras en muros y separación entre juntas.",
        "personas": [
            {"nombre": "Isabel Penagos Agredo", "doc": "29946039", "fecha": "01/01/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Laurentino Agredo", "doc": "50345536", "fecha": "01/01/1960", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "632", "corregimiento": "Las Vegas", "prioridad": "BAJA",
        "observaciones_evaluador": "Daños en repello de muro externo, dilatación en muro y fisuras menores en soportes de cubierta.",
        "personas": [
            {"nombre": "Elmar Gallego", "doc": "27525007", "fecha": "14/08/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Mariela Montealegre", "doc": "29941075", "fecha": "12/02/1971", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Sebastian Montealegre", "doc": "1104821219", "fecha": "05/08/2013", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "633", "corregimiento": "Bellavista", "prioridad": "MEDIA",
        "observaciones_evaluador": "Afectaciones en mampostería y separación de juntas en muros.",
        "personas": [
            {"nombre": "Amanda Lucia Velazco", "doc": "31473903", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "634", "corregimiento": "Campestre Real", "prioridad": "BAJA",
        "observaciones_evaluador": "Elementos estructurales (vigas y columnas) en buen estado, fisuras menores en repello de muros.",
        "personas": [
            {"nombre": "Jorge Arlex Marulanda", "doc": "16735085", "fecha": "09/03/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Daniel Andres Marulanda", "doc": "1006036952", "fecha": "04/08/1998", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "635", "corregimiento": "Campestre Real", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en acabados de muros y repellos.",
        "personas": [
            {"nombre": "Maria Camila Varela Ramirez", "doc": "1144204246", "fecha": "21/06/1997", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Silvia Sandoval", "doc": "31260380", "fecha": "25/04/2009", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "636", "corregimiento": "Santa Ines", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda rural de 3 pisos con daños graves por sismo, muros caídos y alta vulnerabilidad. Inhabitable con recomendación de desalojo inmediato[cite: 58].",
        "personas": [
            {"nombre": "Jhon Alexander Burgo", "doc": "16940570", "fecha": "16/06/1947", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "637", "corregimiento": "Buitrera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras leves en mampostería, sistema estructural en buenas condiciones.",
        "personas": [
            {"nombre": "Isabel Penagos Agredo", "doc": "167335232", "fecha": "01/01/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "638", "corregimiento": "Finlandia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de 3 pisos con grietas horizontales y verticales por desplazamiento en muros y fachada.",
        "personas": [
            {"nombre": "Alba Nubia Velazquez", "doc": "75325169", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 621-638...")
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
        print(f"MIGRACIÓN LOTE 621-638 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
