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
        "num_formulario": "1527", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Ana Luisa Parra y Pedro Luis Carvajal - Afectación residencial, salud vulnerable (RUFE-1527)[cite: 53].",
        "personas": [
            {"nombre": "Ana Luisa Parra", "doc": "29940543", "fecha": "05/02/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Pedro Luis Carvajal Patiño", "doc": "7248997", "fecha": "07/03/1961", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Belen Acevedo", "doc": "1116378015", "fecha": "26/02/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1528", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Gustavo Aparicio y Viviana Aparicio - Reparación de tejado propia, riesgo con pared vecina (RUFE-1528)[cite: 53].",
        "personas": [
            {"nombre": "Gustavo Aparicio", "doc": "78015130", "fecha": "14/11/1952", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Viviana Aparicio", "doc": "1118291190", "fecha": "06/04/1989", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Manvela Arteaga", "doc": "30060087", "fecha": "02/04/1960", "es_jefe": False, "sexo": "F", "parentesco": "Familiar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1529", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Piedad Muñoz Pizarro - Vecina de edificio de 5 pisos a punto de colapsar (RUFE-1529)[cite: 53].",
        "personas": [
            {"nombre": "Piedad Muñoz Pizarro", "doc": "31940003", "fecha": "05/09/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1530", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Elizabeth Martinez Galarza / Eduardo Viña Solis - Adultos mayores, cielorraso averiado y fisura en columna (RUFE-1530)[cite: 53].",
        "personas": [
            {"nombre": "Elizabeth Martinez Galarza", "doc": "38437032", "fecha": "23/03/1956", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Eduardo Viña Solis", "doc": "5497024", "fecha": "11/05/1967", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Diego Delgado Martinez", "doc": "1457588", "fecha": "23/03/1974", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1531", "corregimiento": "Bolívar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Veryined Zuleta Muñoz - Segundo piso, pared exterior fracturada (RUFE-1531)[cite: 53].",
        "personas": [
            {"nombre": "Veryined Zuleta Muñoz", "doc": "31478358", "fecha": "29/11/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Neffer Sofi Zuleta Muñoz", "doc": "1031629497", "fecha": "27/12/1969", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1532", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Edeniver Pabon Astudillo - Parapeto fracturado, habitación con riesgo de colapso (RUFE-1532)[cite: 53].",
        "personas": [
            {"nombre": "Edeniver Pabon Astudillo", "doc": "31467264", "fecha": "12/07/1958", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Miriam Pabon Astudillo", "doc": "31468661", "fecha": "16/08/1962", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1533", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Maria del Pilar Wuman Orejuela - Casa parcialmente colapsada en parte delantera (RUFE-1533)[cite: 53].",
        "personas": [
            {"nombre": "Maria del Pilar Wuman Orejuela", "doc": "31924694", "fecha": "13/11/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Henry Alberto Pachajoa Erazo", "doc": "16448955", "fecha": "05/01/1960", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Cristhian Pachajoa Wuman", "doc": "1144207930", "fecha": "18/09/1998", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1534", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Rubiela Astalza Zambrano - Piso levantado, paredes agrietadas (RUFE-1534)[cite: 53].",
        "personas": [
            {"nombre": "Rubiela Astalza Zambrano", "doc": "31956442", "fecha": "16/11/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diana Marcela Polanco Astalza", "doc": "1118304990", "fecha": "14/08/1995", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Juan Jose Astalza Zambrano", "doc": "1118305604", "fecha": "10/04/1999", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1535", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Sandra Eugenia Zamora Franco - Techo a punto de colapsar, piso levantado (RUFE-1535)[cite: 53].",
        "personas": [
            {"nombre": "Sandra Eugenia Zamora Franco", "doc": "31998022", "fecha": "04/08/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ingrid Juliana Urrea Zamora", "doc": "1193075537", "fecha": "10/12/2001", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1536", "corregimiento": "Yumbo", "prioridad": "ALTA",
        "observaciones_evaluador": "Martha Milena Hurtado Hernandez - Vivienda antigua, paredes fracturadas con deformación (RUFE-1536)[cite: 55].",
        "personas": [
            {"nombre": "Martha Milena Hurtado Hernandez", "doc": "67016021", "fecha": "03/05/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "María Victoria Hurtado Hernandez", "doc": "31974001", "fecha": "26/12/1966", "es_jefe": False, "sexo": "F", "parentesco": "Familiar", "etnia": "Ninguna"},
            {"nombre": "Oscar Marino Riascos Arias", "doc": "6531067", "fecha": "04/07/1965", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1537", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Jakeline Alzate Quintero - Vivienda de bareque con grietas en unión de paredes (RUFE-1537)[cite: 55].",
        "personas": [
            {"nombre": "Jakeline Alzate Quintero", "doc": "31484862", "fecha": "07/03/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Ana Ceiba Quintero Ramirez", "doc": "29978474", "fecha": "21/06/1963", "es_jefe": False, "sexo": "F", "parentesco": "Padre/Madre", "etnia": "Ninguna"},
            {"nombre": "Maira Edelmiro Mejia Quintero", "doc": "1118284234", "fecha": "23/07/1986", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1538", "corregimiento": "Bolívar", "prioridad": "ALTA",
        "observaciones_evaluador": "Ana Celia Velasco - Fractura del fondo y división de pared (RUFE-1538)[cite: 55].",
        "personas": [
            {"nombre": "Ana Celia Velasco", "doc": "31231813", "fecha": "01/01/1950", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jose Leonardo Gonzalez", "doc": "14947936", "fecha": "08/12/1947", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Ernesto Velasco Ortiz", "doc": "14934644", "fecha": "13/08/1947", "es_jefe": False, "sexo": "M", "parentesco": "Familiar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1539", "corregimiento": "Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Nadia Prado - Fractura a nivel inferior de pared en habitaciones (RUFE-1539)[cite: 55].",
        "personas": [
            {"nombre": "Nadia Prado", "doc": "31471888", "fecha": "02/10/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Isabella Prado", "doc": "1118310466", "fecha": "14/11/1998", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1540", "corregimiento": "San Fernando", "prioridad": "BAJA",
        "observaciones_evaluador": "Luz Adriana Rivera - Asentamientos, grietas en baldosas (RUFE-1540)[cite: 55].",
        "personas": [
            {"nombre": "Luz Adriana Rivera", "doc": "29973229", "fecha": "12/10/1983", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jesus David Rivera", "doc": "1192916751", "fecha": "24/12/1999", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1541", "corregimiento": "Techo Azul", "prioridad": "ALTA",
        "observaciones_evaluador": "Alexander Rodallega - Asentamientos, grietas en suelo, inclinación de casa (RUFE-1541)[cite: 55].",
        "personas": [
            {"nombre": "Alexander Rodallega", "doc": "1006193345", "fecha": "05/11/2003", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Angie Vanesa Rodallega", "doc": "1116384501", "fecha": "10/09/1996", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1542", "corregimiento": "Las Cruces", "prioridad": "ALTA",
        "observaciones_evaluador": "Benito Hoyos Muñoz - Dificultad para desplazarse, miembro menor con discapacidad de comunicación (RUFE-1542)[cite: 55].",
        "personas": [
            {"nombre": "Benito Hoyos Muñoz", "doc": "14840009", "fecha": "14/07/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "María Díaz", "doc": "38835020", "fecha": "12/07/1972", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Luz Adriana Hoyos", "doc": "1118297207", "fecha": "26/07/1983", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1543", "corregimiento": "San Fernando", "prioridad": "BAJA",
        "observaciones_evaluador": "Karen Daniela Rivera - Verificado sin grietas estructurales graves (RUFE-1543)[cite: 55].",
        "personas": [
            {"nombre": "Karen Daniela Rivera", "doc": "1118288907", "fecha": "04/10/2005", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Rigoberto Rivera", "doc": "3127981929", "fecha": "01/01/1970", "es_jefe": False, "sexo": "M", "parentesco": "Padre/Madre", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1527-1543...")
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
        print(f"MIGRACIÓN LOTE 1527-1543 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
