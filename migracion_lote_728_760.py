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
        "num_formulario": "728", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Jardín infantil: evaluado por ingenieros, daños mínimos. Falta evaluación de SGRD.",
        "personas": [
            {"nombre": "Hallen Yaveth Marmolejo Mueses", "doc": "1118296813", "fecha": "17/09/1991", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "729", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Enchape de cocina agrietado y columna horizontal del patio agrietada. Apto del 2do piso con grietas.",
        "personas": [
            {"nombre": "Rodrigo Alberto Ramos Vasquez", "doc": "16450421", "fecha": "26/09/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "730", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Cielo falso en mal estado (muy antiguo), gran parte se cayó. Muro del vecino pandeado.",
        "personas": [
            {"nombre": "Maria Pura Villada Polanco", "doc": "29970728", "fecha": "15/07/1938", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "William Saavedra Villada", "doc": "16452582", "fecha": "31/12/1967", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Karol Paola Gonzalez Saavedra", "doc": "1006536599", "fecha": "19/09/2001", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "James Steban Gonzalez Saavedra", "doc": "1006536611", "fecha": "23/03/2000", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Edwin Isaac Tovar Gonzalez", "doc": "1118313697", "fecha": "05/02/2024", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"},
            {"nombre": "Ashly Luciana Tovar Gonzalez", "doc": "1239688794", "fecha": "23/06/2022", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "737", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Grieta mínima en pared de sala a cuarto de dormir. Azulejo de baño agrietado.",
        "personas": [
            {"nombre": "Lucy Gaviria Pabon", "doc": "11182883711", "fecha": "16/02/1988", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "738", "corregimiento": "Uribe", "prioridad": "MEDIA",
        "observaciones_evaluador": "Grietas en muros exteriores e interiores.",
        "personas": [
            {"nombre": "Arturo Vasquez Hernandez", "doc": "16820082", "fecha": "01/01/1970", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Stella Vasquez Hernandez", "doc": "0", "fecha": "01/01/1975", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jose Antonio Vasquez Hernandez", "doc": "0", "fecha": "01/01/1980", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "739", "corregimiento": "Belalcazar", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda intervenida por los propietarios.",
        "personas": [
            {"nombre": "Gloria Adima Fernandez Correa", "doc": "66901490", "fecha": "20/01/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Pablo Gomez Mendez", "doc": "16844405", "fecha": "02/01/1960", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Juan Camilo Montaño Fernandez", "doc": "1193580119", "fecha": "03/10/2003", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ginna Camila Montaño Fernandez", "doc": "1105368927", "fecha": "04/08/2006", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "740", "corregimiento": "Las Americas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con animales domésticos (conejos, perros, gatos).",
        "personas": [
            {"nombre": "Nesenia Vasquez", "doc": "1118292637", "fecha": "24/10/1989", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yisel Rojas Vasquez", "doc": "1109679382", "fecha": "14/01/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Mariana Milagros Bernal Vasquez", "doc": "1101211183", "fecha": "02/05/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Rivera", "doc": "1309884", "fecha": "17/06/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "741", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con afectación menor en mampostería. Prioridad Baja.",
        "personas": [
            {"nombre": "Jhonatan Perez", "doc": "3118284684", "fecha": "21/09/1986", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Perez Buitrago", "doc": "31486993", "fecha": "19/10/1988", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "742", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda evaluada con animales domésticos (gatos y perros).",
        "personas": [
            {"nombre": "Jhoana Agudelo Buitrago", "doc": "1005785485", "fecha": "14/11/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Calder Buitrago", "doc": "3113589205", "fecha": "21/01/2003", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Dayana Buitrago", "doc": "3116866678", "fecha": "13/01/2001", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Delby Buitrago", "doc": "3157841537", "fecha": "31/10/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "743", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado sin novedades mayores.",
        "personas": [
            {"nombre": "Rubimaria Leon", "doc": "31473913", "fecha": "06/02/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nelson Herrera", "doc": "167346952", "fecha": "15/02/1966", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Yulin Herrera", "doc": "1116372585", "fecha": "05/05/2005", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "744", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con prioridad baja verificado.",
        "personas": [
            {"nombre": "Edinson Alejandro Gonzales Lopez", "doc": "1116130659", "fecha": "11/05/1988", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "745", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras menores en mampostería.",
        "personas": [
            {"nombre": "Amparo Vasquez", "doc": "31469183", "fecha": "28/05/1958", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Karen Julieth Vasquez", "doc": "1118282997", "fecha": "12/02/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Dominic Soto", "doc": "1116384829", "fecha": "30/07/2023", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "746", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inspección de mampostería completada sin novedades críticas.",
        "personas": [
            {"nombre": "Ingrid Noguera Betancourth", "doc": "3118285296", "fecha": "12/12/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "747", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda unifamiliar verificada.",
        "personas": [
            {"nombre": "Consuelo Lugo", "doc": "29740917", "fecha": "30/11/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "748", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inspección completada en mampostería no estructural.",
        "personas": [
            {"nombre": "Yamilet Rosero Valencia", "doc": "29740062", "fecha": "02/08/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "749", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda unifamiliar revisada.",
        "personas": [
            {"nombre": "Ana Fernandez", "doc": "25210739", "fecha": "09/10/1945", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "750", "corregimiento": "Las Americas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inspección estructural completada con prioridad baja.",
        "personas": [
            {"nombre": "Roben Davio Fernandez", "doc": "94314648", "fecha": "05/05/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "751", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con agrietamientos superficiales en la fachada.",
        "personas": [
            {"nombre": "Jhon Jairo Fernandez", "doc": "94513882", "fecha": "02/09/1978", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Isabela Fernandez", "doc": "1110042835", "fecha": "02/06/2007", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Vancia Helena Dorado Lopez", "doc": "31486236", "fecha": "10/07/1982", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "752", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda revisada sin afectaciones mayores.",
        "personas": [
            {"nombre": "Maria Greis Palechor", "doc": "66924418", "fecha": "19/09/1973", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juan Pablo Agudelo Palechor", "doc": "1104805313", "fecha": "19/08/2005", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Gleis Kelly Agudelo Palechor", "doc": "1005705271", "fecha": "20/04/2001", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Brayan Stiven Agudelo Quintero", "doc": "1006435707", "fecha": "23/12/2001", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Hectos de Jesus Agudelo Sanchez", "doc": "1387770", "fecha": "31/03/1936", "es_jefe": False, "sexo": "M", "parentesco": "Padre", "etnia": "Ninguna"},
            {"nombre": "Felix Agudelo Gallego", "doc": "6551250", "fecha": "25/02/1963", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "753", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de material revisada, sin novedades estructurales graves.",
        "personas": [
            {"nombre": "Maritza Hellinda Viveros Garcia", "doc": "29978443", "fecha": "11/12/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "754", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras menores y habitabilidad supervisada.",
        "personas": [
            {"nombre": "Fabian Camacho Beltran", "doc": "1118301112", "fecha": "18/04/1993", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Pimi Beltran", "doc": "1006778241", "fecha": "27/10/2001", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Salome Camacho Beltran", "doc": "1118311649", "fecha": "16/08/2017", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "755", "corregimiento": "Buenos Aires - La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble evaluado con prioridad baja.",
        "personas": [
            {"nombre": "Olga Cristina Goyes Bastidas", "doc": "31474847", "fecha": "01/12/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Edgar Orlando Bolivar Medina", "doc": "94306083", "fecha": "04/08/1969", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Julieth Bolivar Goyes", "doc": "1118807597", "fecha": "19/07/1996", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Gabriel Matias Reyes Bolivar", "doc": "1116380153", "fecha": "19/09/2016", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "756", "corregimiento": "Campestre Real", "prioridad": "BAJA",
        "observaciones_evaluador": "Apartamento verificado con fisuras menores en acabados.",
        "personas": [
            {"nombre": "Alexander Suaza Cardona", "doc": "94296683", "fecha": "20/11/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diana Aimena Garcia", "doc": "25171772", "fecha": "19/01/1977", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Emmanuel Suaza Garcia", "doc": "111484922", "fecha": "06/11/2012", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Garcia Rodriguez", "doc": "94402786", "fecha": "10/08/1973", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "757", "corregimiento": "Lleras", "prioridad": "BAJA",
        "observaciones_evaluador": "Apartamento en edificio con revisiones de acabados completada.",
        "personas": [
            {"nombre": "Cristian Ortiz", "doc": "1118300557", "fecha": "01/06/1993", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "758", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado con prioridad baja.",
        "personas": [
            {"nombre": "Anderson Tovar", "doc": "1118283903", "fecha": "01/07/1986", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yarima Gomez", "doc": "31486501", "fecha": "30/11/1982", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Tomas Tovar", "doc": "1150687195", "fecha": "19/11/2009", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "T1010 Tovar", "doc": "1111488239", "fecha": "19/12/2020", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "759", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de material con revisión de juntas y muros completada.",
        "personas": [
            {"nombre": "Israel Villa", "doc": "193367337", "fecha": "16/04/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andres Mauricio Villa", "doc": "1118309002", "fecha": "22/02/1997", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "760", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de material con fisuras superficiales en muros y repellos.",
        "personas": [
            {"nombre": "Yhon Elisio Calpa Sanchez", "doc": "1062775279", "fecha": "13/01/1988", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Aida Mercedez Sanchez Sanchez", "doc": "1062776719", "fecha": "15/09/1987", "es_jefe": False, "sexo": "F", "parentesco": "Esposo(a)", "etnia": "Ninguna"},
            {"nombre": "Yisel Valeria Calpa Sanchez", "doc": "1062777747", "fecha": "26/11/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Dillan Felipe Calpa Sanchez", "doc": "1105387788", "fecha": "15/12/2013", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 728-760...")
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
        print(f"MIGRACIÓN LOTE 728-760 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
