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
        "num_formulario": "496", "corregimiento": "San Jorge", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en pórticos de concreto reforzado. Elementos estructurales sin daños que comprometan la seguridad. Habitable.",
        "personas": [
            {"nombre": "Isabel Cortazar", "doc": "7006016621", "fecha": "07/10/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "497", "corregimiento": "Gaitan", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras en muros divisorios. Habitable.",
        "personas": [
            {"nombre": "Ana Julia Bahos Pizarro", "doc": "41646460", "fecha": "17/09/1954", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "498", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Edificio con afectaciones menores en cielo raso y fisuras en juntas. Habitable.",
        "personas": [
            {"nombre": "Harold Reyes", "doc": "16774969", "fecha": "23/08/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Elena Sierra", "doc": "63489613", "fecha": "23/12/1973", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Santiago Reyes", "doc": "1007489384", "fecha": "18/10/2000", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Isabela Reyes", "doc": "1007541793", "fecha": "15/01/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "499", "corregimiento": "Gaitan", "prioridad": "ALTA",
        "observaciones_evaluador": "Cubierta de la terraza del 2o al 3er piso con fisuras menores en paredes y riesgo de caída.",
        "personas": [
            {"nombre": "Nancy Ovalle", "doc": "31626851", "fecha": "23/04/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Over Imanalla Prado", "doc": "16627476", "fecha": "05/01/1992", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "500", "corregimiento": "Nueva Estancia", "prioridad": "ALTA",
        "observaciones_evaluador": "Hogar con afectaciones en diferentes zonas, muros portantes y vigas con daños estructurales en mampostería.",
        "personas": [
            {"nombre": "Isabel Cortazar", "doc": "1006016621", "fecha": "26/12/2002", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "501", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material y bahareque, con muro perimetral colindante con casa vecina descolgado y riesgo. Muros divisorios fisurados.",
        "personas": [
            {"nombre": "Carlos Andres Perez", "doc": "16455772", "fecha": "19/07/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Billy Oviedo", "doc": "0", "fecha": "01/01/1975", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "502", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en bahareque con fisuras y desprendimiento de enchapado en muros y juntas. Habitable.",
        "personas": [
            {"nombre": "Leidy Carvajal", "doc": "1115420631", "fecha": "21/08/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Oliver Giraldo", "doc": "1115418303", "fecha": "26/11/1985", "es_jefe": False, "sexo": "M", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Karen Sofia Giraldo", "doc": "1115421024", "fecha": "13/05/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Emiliana Giraldo", "doc": "1115424912", "fecha": "23/06/2023", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "503", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras y grietas mínimas en puertas y ventanas, techos corridos de la cubierta. Habitable.",
        "personas": [
            {"nombre": "Joselin Andrea Gonzalez", "doc": "1144163875", "fecha": "23/11/1992", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Emilio Ospina", "doc": "1109684927", "fecha": "23/05/2018", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Martin Ospina", "doc": "1109939246", "fecha": "30/08/2021", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "504", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras y grietas. Puertas y ventanas no presentan fallas. Habitable.",
        "personas": [
            {"nombre": "Judit Tovar", "doc": "52009303", "fecha": "01/01/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "505", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en bahareque con desprendimientos de material pequeños y colapso parcial del muro de atrás. Fisuras mínimas en juntas.",
        "personas": [
            {"nombre": "Judit Tovar", "doc": "52009303", "fecha": "01/01/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "506", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material con desprendimiento de revoque y grietas. Muro con grietas considerables, se recomienda tumbar y hacer de nuevo.",
        "personas": [
            {"nombre": "Francia Castillo", "doc": "31489046", "fecha": "02/12/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "507", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras mínimas en pared del baño y tejas corridas de la cubierta. Sin riesgo latente, habitable.",
        "personas": [
            {"nombre": "Dersio Piraza", "doc": "1004030419", "fecha": "21/05/1994", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sandalina Perdiz", "doc": "1028180384", "fecha": "02/03/1998", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Alan Piraza", "doc": "31477803", "fecha": "11/05/1975", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Amanda Peraz", "doc": "0", "fecha": "01/01/1975", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "508", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material con grieta en un elemento estructural (columna), se percibe poco acero estructural. Se recomienda refuerzo estructural.",
        "personas": [
            {"nombre": "Ana Julia Artundiaga", "doc": "31960013", "fecha": "18/02/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "509", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con estuco y fisuras mínimas en muros. Pequeños desprendimientos. Habitable.",
        "personas": [
            {"nombre": "Mayerli Muñoz", "doc": "106537286", "fecha": "30/01/1998", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diego Fernando Gerena", "doc": "1118295844", "fecha": "03/05/1991", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Salome Gerena", "doc": "116378958", "fecha": "19/04/2015", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "510", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de bahareque con sus muros colapsados y soportes debilitados. Riesgo latente.",
        "personas": [
            {"nombre": "Claudia Fonseca Solis", "doc": "1006876379", "fecha": "26/05/1997", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Miralba Solis", "doc": "31483165", "fecha": "20/08/1976", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Bridge Vanesa Fonseca Solis", "doc": "14463777526", "fecha": "21/10/2013", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "511", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Casa colapsada. Requiere desalojo inmediato.",
        "personas": [
            {"nombre": "Lubian Sanchez", "doc": "2693389", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "512", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda destruida. Alto riesgo.",
        "personas": [
            {"nombre": "Feliciana Guampe", "doc": "38959300", "fecha": "20/01/1942", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jose Antonio Ramirez Garcia", "doc": "1130673886", "fecha": "23/10/1987", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "513", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda destruida con riesgo de colapso, sistema estructural averiado.",
        "personas": [
            {"nombre": "Leonardo Gomez", "doc": "6342687", "fecha": "21/11/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Isabel Gomez", "doc": "1006337807", "fecha": "17/03/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Johanny Gomez", "doc": "1114481704", "fecha": "26/11/1989", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Joan Santiago Gomez", "doc": "1232791605", "fecha": "26/02/2015", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Sebastian Gomez", "doc": "1118313171", "fecha": "14/11/2021", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "514", "corregimiento": "La Paz", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque colapsada. Propietario en alto riesgo.",
        "personas": [
            {"nombre": "Luis Alirio Garzon", "doc": "4676127", "fecha": "23/02/1953", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "515", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque con alto riesgo de colapso en muros y cubierta.",
        "personas": [
            {"nombre": "Blanca Ruth Hernandez Ocampo", "doc": "29067290", "fecha": "29/01/1935", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Raul Hernandez Ocampo", "doc": "16359341", "fecha": "21/01/1964", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "516", "corregimiento": "Buitrera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con mampostería afectada en un sistema estructural. Con averías en columna y vigas a reconstruir y reforzar.",
        "personas": [
            {"nombre": "Zeneida Lozada Aguirre", "doc": "31471274", "fecha": "24/02/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Francisco Cordoba", "doc": "16448689", "fecha": "06/09/1959", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "517", "corregimiento": "Miravalle Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda afectada estructuralmente en unión de columna y viga. Reparable.",
        "personas": [
            {"nombre": "Oswaldo Ocampo", "doc": "16791649", "fecha": "20/07/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "518", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con mampostería comprometida por volumen de tierra apoyado en la misma.",
        "personas": [
            {"nombre": "Anizar Urbano", "doc": "16463446", "fecha": "12/05/1983", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Michel Urbano", "doc": "1116373416", "fecha": "30/12/2006", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Tiago Martinez", "doc": "1239688917", "fecha": "3/1/2023", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Jose Antonio Urbano", "doc": "116377999", "fecha": "15/02/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Cindy Guevara", "doc": "1118286075", "fecha": "08/02/1987", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "519", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda unifamiliar construida empíricamente con riesgo de colapso inminente.",
        "personas": [
            {"nombre": "Karla Estefania Lemos Muñoz", "doc": "1143841776", "fecha": "12/01/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Eristina Lemos Muñoz", "doc": "66997212", "fecha": "15/04/1977", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Limbania Muñoz Gutierrez", "doc": "66833591", "fecha": "01/01/1970", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Juan Gregorio Lemos", "doc": "94426239", "fecha": "20/01/1970", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "520", "corregimiento": "Buitrera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material con fisuras y grietas en parte de la mampostería, con muros portantes afectados.",
        "personas": [
            {"nombre": "Luis Fernando Hoyos Guzman", "doc": "1118294002", "fecha": "18/04/1990", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Ermila Guzman", "doc": "16460567", "fecha": "24/07/1980", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Olga Lucia Samboni Hoyos", "doc": "1192728994", "fecha": "04/01/2002", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Deisa Fernanda Samboni Hoyos", "doc": "1118304693", "fecha": "22/03/1995", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Wilmer Samboni", "doc": "1007529398", "fecha": "28/10/1999", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 496-520...")
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
        print(f"MIGRACIÓN LOTE 496-520 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
