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
        "num_formulario": "593", "corregimiento": "Belalcazar", "prioridad": "ALTA",
        "observaciones_evaluador": "Demolición de 4to piso, mampostería y vigas afectadas por sismo.",
        "personas": [
            {"nombre": "Alex Calderon", "doc": "16454553", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "594", "corregimiento": "Arroyohondo", "prioridad": "ALTA",
        "observaciones_evaluador": "Columnas y vigas con daños graves, área posterior en peligro de colapso y recomendación de demolición de muros.",
        "personas": [
            {"nombre": "Adriano Ramos Salazar", "doc": "629940416", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "595", "corregimiento": "Belalcazar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mampostería con fisuras, desprendimiento de revestimiento, se requiere demolición del muro frontal del segundo piso.",
        "personas": [
            {"nombre": "Adriana Patricia Arango", "doc": "31474471", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "596", "corregimiento": "Bellavista", "prioridad": "ALTA",
        "observaciones_evaluador": "Muro de la habitación en riesgo de colapso; se requiere demolición urgente de muros afectados.",
        "personas": [
            {"nombre": "Zeneida Mesa Salas", "doc": "629401106", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "597", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en superboard con fisuras superficiales y desprendimiento de revestimiento. Habitable con precaución.",
        "personas": [
            {"nombre": "Kelly Viviana Quintana", "doc": "1118310384", "fecha": "06/12/1998", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Kylian Joao Sandobal Aragon", "doc": "1118313342", "fecha": "01/07/2023", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "598", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras estéticas y desprendimiento leve de estuco y baldosa en fachada.",
        "personas": [
            {"nombre": "Marilyn Muñoz", "doc": "166988617", "fecha": "01/01/1977", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "600", "corregimiento": "Trinidad", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con cielo raso colapsado y cubierta rodada, sin afectaciones estructurales mayores.",
        "personas": [
            {"nombre": "Juliana Murillo Moreno", "doc": "1118306979", "fecha": "30/06/1996", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Monica Becerra", "doc": "31480680", "fecha": "08/05/1976", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "601", "corregimiento": "Trinidad", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grietas de gran magnitud en muros, desprendimiento en el baño. Estructura sin riesgo inminente, habitable tras intervención.",
        "personas": [
            {"nombre": "Martha Lucia Castillo", "doc": "31907605", "fecha": "26/01/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "602", "corregimiento": "San Fernando", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda de material con fisuras en columnas; se recomienda retirar el revoque para tratar grietas.",
        "personas": [
            {"nombre": "Lina Valencia", "doc": "1118294265", "fecha": "23/03/1997", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juan Felipe Daza", "doc": "1104835091", "fecha": "18/04/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Cesar Valencia", "doc": "16530972", "fecha": "19/08/1964", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"},
            {"nombre": "Juan David Valencia", "doc": "1193233661", "fecha": "05/02/1999", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "603", "corregimiento": "El Pedregal", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en bahareque con fisuras y desprendimiento de revestimiento en una habitación.",
        "personas": [
            {"nombre": "Soraida Rivera Aranzazu", "doc": "31927454", "fecha": "27/02/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Valeria Gomez Aranzazu", "doc": "0", "fecha": "19/08/2015", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ian Rivera Aranzazu", "doc": "0", "fecha": "08/02/2023", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Diego Aranzazu", "doc": "94529455", "fecha": "24/04/1989", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Julieth Fernanda Aranzazu", "doc": "118293262", "fecha": "10/02/1990", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "604", "corregimiento": "Belalcazar", "prioridad": "ALTA",
        "observaciones_evaluador": "Desprendimiento de estructura metálica del cielo raso y grietas horizontales/verticales en muros y de repello.",
        "personas": [
            {"nombre": "Jhon Jairo Maceda", "doc": "16463918", "fecha": "01/01/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "605", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras estéticas en mampostería, desprendimiento de estuco. Estructura externa en buen estado.",
        "personas": [
            {"nombre": "Catalino Romero", "doc": "182837945", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "606", "corregimiento": "Bellavista", "prioridad": "ALTA",
        "observaciones_evaluador": "Grietas horizontales y diagonales en el muro de fachada del segundo piso; separación de juntas.",
        "personas": [
            {"nombre": "Carolina Sotizabal", "doc": "1118288598", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "607", "corregimiento": "Miravalle", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muros internos con desprendimiento de revestimiento y separación en juntas de mampostería.",
        "personas": [
            {"nombre": "Jose Leider Gutierrez", "doc": "11114481270", "fecha": "01/01/1985", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Milena Gutierrez", "doc": "2547115", "fecha": "01/01/1988", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "608", "corregimiento": "Buitrera La Esperanza", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en material con fisuras y grietas graves en muros y columnas. No habitable.",
        "personas": [
            {"nombre": "Diomr Ureña Acuña", "doc": "38996945", "fecha": "14/09/1947", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Thonaith An Ureña Acuña", "doc": "16461974", "fecha": "20/08/1981", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "609", "corregimiento": "Manga Vieja El Chochó", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en madera con fisura grave por el sismo. Requiere reparación. Integrante con esquizofrenia y padre postrado en cama.",
        "personas": [
            {"nombre": "Maria Mabel Lozada", "doc": "38280647", "fecha": "20/04/1959", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luis Albero Poveda", "doc": "5932642", "fecha": "01/01/1950", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Maribel Poveda Lozada", "doc": "31579521", "fecha": "22/05/1980", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Josue Poveda Lozada", "doc": "0", "fecha": "18/07/2015", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "610", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque con muros colapsados y soportes debilitados. Vivienda inhabitable.",
        "personas": [
            {"nombre": "Alberto Lopez Giraldo", "doc": "6523704", "fecha": "01/04/1955", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jimmy Lopez Giraldo", "doc": "0", "fecha": "01/01/1985", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "611", "corregimiento": "Santa Ines", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda rural de 1 piso en bahareque en muy mal estado, con muro colapsado y requerimiento de reconstrucción en ladrillo.",
        "personas": [
            {"nombre": "Nelson Polanco", "doc": "6341605", "fecha": "22/09/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yolanda Noguera Perez", "doc": "29756562", "fecha": "01/01/1968", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Nelson David Perez Noguera", "doc": "1116379027", "fecha": "22/05/2015", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "612", "corregimiento": "Buitrera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda rural de 1 piso en ladrillo sin confinamiento, con fisuras en paredes y posible asentamiento de vigas.",
        "personas": [
            {"nombre": "Jaime Velasco", "doc": "16445111", "fecha": "12/05/1951", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ofir Hencio Morales", "doc": "31465647", "fecha": "16/04/1956", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "613", "corregimiento": "Dapa El Chochó", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda rural de 2 pisos con fisuras en mampostería y cielo raso, requiere inspección estructural.",
        "personas": [
            {"nombre": "Sonia Felicia Tintinago", "doc": "66905925", "fecha": "14/03/1974", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Tulio Muñoz", "doc": "15814046", "fecha": "07/10/1972", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Timotea Muñoz Tintinago", "doc": "31223279", "fecha": "09/08/1947", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"},
            {"nombre": "Isabella Muñoz Tintinago", "doc": "1106377301", "fecha": "10/03/2010", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "614", "corregimiento": "Buenos Aires", "prioridad": "BAJA",
        "observaciones_evaluador": "Apartamento interno en bahareque totalmente inhabitable a punto de caerse.",
        "personas": [
            {"nombre": "Blanca Liliana Serna Jurado", "doc": "31945399", "fecha": "28/02/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "615", "corregimiento": "Santa Ines", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda de dos pisos con problemas en la estructura del primer piso por falta de columnas y vigas, y techo con inminente riesgo de colapso.",
        "personas": [
            {"nombre": "Oracio Arnulfo Gil Durango", "doc": "694504933", "fecha": "21/02/1986", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Mireya Caicedo Velaz", "doc": "29973816", "fecha": "28/02/1962", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Cristobal Gil Caicedo", "doc": "1116381073", "fecha": "08/05/2007", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "616", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muros confinados superficiales, cielo raso desprendido.",
        "personas": [
            {"nombre": "Carmen Rosa Luna Garzon", "doc": "31467274", "fecha": "12/06/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Helmud Moreno", "doc": "0", "fecha": "01/01/1965", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Jennifer Moreno", "doc": "0", "fecha": "01/01/1995", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Sebastian Moreno", "doc": "0", "fecha": "01/01/2005", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "617", "corregimiento": "Lleras", "prioridad": "ALTA",
        "observaciones_evaluador": "Muro de fachada con posibilidad de colapso y afectación en la estructura.",
        "personas": [
            {"nombre": "Yesid Palomino Benitez", "doc": "6531089", "fecha": "13/12/1987", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andria Paola Velez Castro", "doc": "329940041", "fecha": "20/02/1965", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "618", "corregimiento": "Lleras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras en la parte interna de la placa y desprendimiento de revestimiento en el baño.",
        "personas": [
            {"nombre": "Doris Bolaños", "doc": "31473010", "fecha": "01/06/1987", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jose Libardo Prado", "doc": "6493917", "fecha": "01/01/1970", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Maria Jose Motato Riascos", "doc": "1116379226", "fecha": "01/01/2010", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Zamara Motato Riascos", "doc": "0", "fecha": "01/01/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "619", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras estéticas de mampostería, baldosas desprendidas y desprendimiento de repello en la fachada del segundo piso.",
        "personas": [
            {"nombre": "Elizabeth Martinez", "doc": "16450369", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "620", "corregimiento": "Lleras", "prioridad": "ALTA",
        "observaciones_evaluador": "Estructura colapsada parcialmente en terraza, muros agrietados y caídos, con requerimiento de reforzamiento estructural urgente.",
        "personas": [
            {"nombre": "Sarah Mitreya Torres", "doc": "31474998", "fecha": "12/06/1997", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andres Felipe Torres Angel", "doc": "1144178906", "fecha": "17/07/1995", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Ariana Calvo Cifuentes", "doc": "1232829011", "fecha": "17/12/2023", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 593-620...")
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
        print(f"MIGRACIÓN LOTE 593-620 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
