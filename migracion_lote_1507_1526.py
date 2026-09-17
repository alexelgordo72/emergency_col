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
        "num_formulario": "1507", "corregimiento": "Cruces Alta", "prioridad": "BAJA",
        "observaciones_evaluador": "Hoyos Muñoz Benito - Afectación menor en estructura habitacional (RUFE-1507)[cite: 55].",
        "personas": [
            {"nombre": "Benito Hoyos Muñoz", "doc": "11840009", "fecha": "01/01/1966", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Flor Maria Arce", "doc": "3883502", "fecha": "01/01/1964", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Alba Maria Hoyos Dias", "doc": "1118297203", "fecha": "26/06/1983", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1508", "corregimiento": "Nuevo Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Alba Lidia Quiñones - Escaleras al segundo piso derrumbadas, colapso parcial del techado (RUFE-1508)[cite: 55].",
        "personas": [
            {"nombre": "Alba Lidia Quiñones", "doc": "31486583", "fecha": "02/05/1963", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Emanuel Andre Quiñones", "doc": "1116375001", "fecha": "27/09/2007", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Visa Fernanda Quiñones", "doc": "1007779297", "fecha": "26/02/1998", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1509", "corregimiento": "Pizarro", "prioridad": "BAJA",
        "observaciones_evaluador": "German Alviz Castro - Inmueble con afectaciones leves (RUFE-1509)[cite: 55].",
        "personas": [
            {"nombre": "German Alviz Castro", "doc": "16271790", "fecha": "15/02/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Margarita Pamba Paz", "doc": "31153088", "fecha": "25/10/1959", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Elizabeth Alviz Frances", "doc": "1118301444", "fecha": "15/11/1993", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1510", "corregimiento": "Carlos León Dizorro", "prioridad": "BAJA",
        "observaciones_evaluador": "Fabian Hector Pachappa Erazo - Inmueble residencial con fisuras mínimas (RUFE-1510)[cite: 55].",
        "personas": [
            {"nombre": "Fabian Hector Pachappa Erazo", "doc": "16703422", "fecha": "17/09/1964", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Martha Isabel Velazio Lozada", "doc": "67013454", "fecha": "08/01/1998", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Fabian David Pachappa Velasco", "doc": "1105388444", "fecha": "01/02/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1511", "corregimiento": "Carlos León Piroto", "prioridad": "BAJA",
        "observaciones_evaluador": "Marion Consuelo Gueche Paredes - Núcleo familiar registrado sin riesgos mayores (RUFE-1511)[cite: 55].",
        "personas": [
            {"nombre": "Marion Consuelo Gueche Paredes", "doc": "29741702", "fecha": "08/05/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1512", "corregimiento": "San José", "prioridad": "BAJA",
        "observaciones_evaluador": "Alexander Arias - Inmueble residencial verificado (RUFE-1512)[cite: 55].",
        "personas": [
            {"nombre": "Alexander Arias", "doc": "16927744", "fecha": "25/05/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Tatiana Andrea Ayala", "doc": "1112107116", "fecha": "26/12/1997", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Henry Ayala", "doc": "6113934", "fecha": "01/05/1947", "es_jefe": False, "sexo": "M", "parentesco": "Padre/Madre", "etnia": "Ninguna"},
            {"nombre": "Luz Marina Restrepo", "doc": "324863679", "fecha": "01/01/1950", "es_jefe": False, "sexo": "F", "parentesco": "Padre/Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1513", "corregimiento": "San José", "prioridad": "BAJA",
        "observaciones_evaluador": "Valentina Trujillo - Vivienda con grietas leves en diferentes lugares (RUFE-1513)[cite: 55].",
        "personas": [
            {"nombre": "Valentina Trujillo", "doc": "1118308019", "fecha": "22/02/1997", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jesus Alberto Ruiz Sanchez", "doc": "1118303647", "fecha": "01/12/1994", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Ma Victoria Ruiz Trujillo", "doc": "1191224723", "fecha": "28/10/2021", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1514", "corregimiento": "San José", "prioridad": "ALTA",
        "observaciones_evaluador": "Luis Antonio - Vivienda con fisuras en diferentes partes (RUFE-1514)[cite: 55].",
        "personas": [
            {"nombre": "Luis Antonio", "doc": "10475491", "fecha": "10/05/1940", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sandra Ines Gil", "doc": "34599440", "fecha": "22/01/1969", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Angie Marcela Alvear", "doc": "1118303146", "fecha": "23/09/1994", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1515", "corregimiento": "Nuevo Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Lot Melida Campo - Daños estructurales, derrumbe por rocas y techo averiado, daño de cocina por deslizamiento (RUFE-1515)[cite: 56].",
        "personas": [
            {"nombre": "Lot Melida Campo", "doc": "34797382", "fecha": "30/06/1979", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Arneyo Deless Hernandez", "doc": "14880003", "fecha": "18/07/1950", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1516", "corregimiento": "Ivan Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Hayra Rosalba Cosamochin - Casa con fisuras, parte de pared despegada y daño en columna del segundo piso (RUFE-1516)[cite: 56].",
        "personas": [
            {"nombre": "Hayra Rosalba Cosamochin", "doc": "1118303024", "fecha": "23/01/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Enrique Valdes", "doc": "1118300406", "fecha": "16/05/1993", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Hilary Sofia Valdes Cosamac", "doc": "1116376314oj", "fecha": "23/10/2011", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1517", "corregimiento": "Novo Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Michael Brayden Obando - Parte frontal afectada y pequeño derrumbe al caerse la fachada (RUFE-1517)[cite: 56].",
        "personas": [
            {"nombre": "Michael Brayden Obando", "doc": "148309796", "fecha": "01/05/1998", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Laiolet Ortega Obando", "doc": "146381328", "fecha": "01/01/2000", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1518", "corregimiento": "La Trinidad", "prioridad": "MEDIA",
        "observaciones_evaluador": "Plexis Bedoya Palacios - Grietas cerca a tubería de gas y en varios lugares de la casa (RUFE-1518)[cite: 56].",
        "personas": [
            {"nombre": "Plexis Bedoya Palacios", "doc": "16458693", "fecha": "28/07/1979", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yaritza", "doc": "4863890", "fecha": "27/06/1988", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Hornadyz", "doc": "6467834", "fecha": "25/12/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1519", "corregimiento": "San Fe_o", "prioridad": "BAJA",
        "observaciones_evaluador": "Martin Stevan Sandoval - Vivienda de 2 pisos, segunda planta y muros externos afectados, problemas de escalera (RUFE-1519)[cite: 56].",
        "personas": [
            {"nombre": "Martin Stevan Sandoval", "doc": "1118288376", "fecha": "03/03/1987", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jesica Bolaño", "doc": "1118288140", "fecha": "05/12/1988", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Sharail Sandoval", "doc": "1116377948", "fecha": "02/02/2016", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Stevan Sandoval", "doc": "1116380266", "fecha": "26/10/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1520", "corregimiento": "Cruces Alta", "prioridad": "ALTA",
        "observaciones_evaluador": "Aally Vanesa Riasco - Casa dañada en piezas y baño por terreno suelto, fisuras en el piso (RUFE-1520)[cite: 57].",
        "personas": [
            {"nombre": "Aally Vanesa Riasco", "doc": "1007976780", "fecha": "05/11/2003", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alexander Rodallega", "doc": "1006193345", "fecha": "10/09/1969", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1521", "corregimiento": "Cruces Alta", "prioridad": "ALTA",
        "observaciones_evaluador": "Gloria Amparo Marin Arias - Alto riesgo, casa de madera con guaduas partidas, piso rajado en cocina, derrumbe parcial de paredes (RUFE-1521)[cite: 57].",
        "personas": [
            {"nombre": "Gloria Amparo Marin Arias", "doc": "31966255", "fecha": "15/01/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1522", "corregimiento": "Carlos León Dizorro", "prioridad": "ALTA",
        "observaciones_evaluador": "Robinson Sanchez Campazono - Vivienda con fisuras y daños considerables (RUFE-1522)[cite: 57].",
        "personas": [
            {"nombre": "Robinson Sanchez Campazono", "doc": "94314546", "fecha": "22/09/1971", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Patricia Acero Paz", "doc": "31534709", "fecha": "03/08/1974", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Lina Marcela Sánchez Acero", "doc": "1118303060", "fecha": "18/09/1994", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1523", "corregimiento": "Pizarro", "prioridad": "ALTA",
        "observaciones_evaluador": "Alexander Castillo - Inmueble con afectación residencial crítica (RUFE-1523)[cite: 57].",
        "personas": [
            {"nombre": "Alexander Castillo", "doc": "16403939", "fecha": "01/01/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nancy Elizabeth Maldonado", "doc": "3168010596", "fecha": "01/05/1962", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1524", "corregimiento": "Pizarro", "prioridad": "ALTA",
        "observaciones_evaluador": "Rubial Guerrero Senca - Inmueble con daños residenciales (RUFE-1524)[cite: 57].",
        "personas": [
            {"nombre": "Rubial Guerrero Senca", "doc": "6252233", "fecha": "01/04/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Stella Garzón Henao", "doc": "29827151", "fecha": "02/12/1964", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Nadia Fernanda Guerrero Garzón", "doc": "1118302174", "fecha": "13/04/1994", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1525", "corregimiento": "San Fe_o", "prioridad": "ALTA",
        "observaciones_evaluador": "Maria Edilma Gonzalez - Casa de lata y esterilla, techo de zinc con estructura de guadua y plástico (RUFE-1525)[cite: 57].",
        "personas": [
            {"nombre": "Maria Edilma Gonzalez", "doc": "29432540", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1526", "corregimiento": "Honda", "prioridad": "ALTA",
        "observaciones_evaluador": "Efrain Marquez - Vivienda de 2 pisos con afectación grave de fisuras en muros, sin confinamiento estructural, riesgo alto de colapso (RUFE-1526)[cite: 57].",
        "personas": [
            {"nombre": "Efrain Marquez", "doc": "6207695", "fecha": "01/01/1966", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sorongela", "doc": "39564700", "fecha": "12/12/1969", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1507-1526...")
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
        print(f"MIGRACIÓN LOTE 1507-1526 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
