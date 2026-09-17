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
        "num_formulario": "761", "corregimiento": "Belalcazar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Edificio con local comercial que sufre averías y riesgo en cubierta y fachada.",
        "personas": [
            {"nombre": "Maria Elena Mejia", "doc": "31831496", "fecha": "14/12/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "762", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con mampostería afectada en un 30% en muros no confinados y daños en chimenea[cite: 69].",
        "personas": [
            {"nombre": "Alex Hernando Gonzales Aguilar", "doc": "79371099", "fecha": "02/09/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alba Monica Aragón Leal", "doc": "31998918", "fecha": "15/04/1969", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Kamilo Andres Gonzales Aragón", "doc": "1109921300", "fecha": "20/05/2006", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "763", "corregimiento": "Finlandia", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda unifamiliar con mampostería afectada en un 50% y cubierta de panel yeso.",
        "personas": [
            {"nombre": "Raquel Adriana Triviño Rincón", "doc": "66873567", "fecha": "15/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Cristhian Mora Triviño", "doc": "1193592308", "fecha": "03/06/2003", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Valentina Mora Triviño", "doc": "1113790001", "fecha": "21/02/2005", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "764", "corregimiento": "Trinidad", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en mampostería con afectaciones menores (40%), se requiere visita de ingeniero estructural y revisión de vigas perimetrales.",
        "personas": [
            {"nombre": "Juan Carlos Varela Delgado", "doc": "16457286", "fecha": "29/10/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Diana Vanessa Cardozo Flores", "doc": "1118286538", "fecha": "04/05/1986", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Ethan Varela Cardozo", "doc": "0", "fecha": "20/11/2020", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ami Belen Varela Cardozo", "doc": "0", "fecha": "10/05/2025", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "765", "corregimiento": "Trinidad", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras horizontales y diagonales en el segundo piso.",
        "personas": [
            {"nombre": "Diana Triviño", "doc": "66872687", "fecha": "21/12/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Alberto Escobar", "doc": "16182683", "fecha": "01/01/1975", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Carlos Alexander Escobar Triviño", "doc": "1104832288", "fecha": "19/03/2013", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "766", "corregimiento": "Las Vegas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Mampostería medianamente afectada en un 80% (requiere cambio de pared)[cite: 70].",
        "personas": [
            {"nombre": "Luz Angela Muñoz Ortiz", "doc": "38552436", "fecha": "07/07/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Karen Sofia Ospina Muñoz", "doc": "1118308833", "fecha": "17/08/1997", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "767", "corregimiento": "Miravalle Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Institución educativa con afectaciones en la losa por asentamiento, escaleras fisuradas y losa de comedor desprendida[cite: 70].",
        "personas": [
            {"nombre": "Katherine Franco Muñoz", "doc": "31567617", "fecha": "13/02/1981", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "768", "corregimiento": "El Rodadero", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda estructuralmente estable con averías en mampostería y contención colapsada[cite: 70].",
        "personas": [
            {"nombre": "Joan de Jesus Lopez Bernal", "doc": "94255594", "fecha": "10/12/1968", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "John Edinson Rivera Astudillo", "doc": "1061531708", "fecha": "13/04/1988", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Zorayda Ruiz Torres", "doc": "166863455", "fecha": "01/01/1974", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "769", "corregimiento": "Miravalle", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con daños menores y mampostería supervisada.",
        "personas": [
            {"nombre": "Nury Margot Parraex", "doc": "31482989", "fecha": "11/12/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "770", "corregimiento": "Rincon Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda prefabricada con sistema estructural combinado, presenta fisuras y requiere corrección oportuna.",
        "personas": [
            {"nombre": "Norelsy Urrutia", "doc": "25628452", "fecha": "22/04/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luisa Fernanda Coatin", "doc": "1088650490", "fecha": "23/07/2001", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Erick Santiago Coatin", "doc": "1104845506", "fecha": "17/08/2019", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "771", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Muros prestados gravemente afectados; recomendación de demolición y evacuación[cite: 71].",
        "personas": [
            {"nombre": "Magdalena Buitrago", "doc": "22108246", "fecha": "01/12/1955", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jorge Albeiro Buitrago", "doc": "98561575", "fecha": "25/05/1971", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "772", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble evaluado con prioridad media.",
        "personas": [
            {"nombre": "Rosalba Muñoz", "doc": "29580188", "fecha": "11/11/1954", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "773", "corregimiento": "Montañitas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Edificación con afectaciones en unión de columna con viga.",
        "personas": [
            {"nombre": "Amanda Martinez", "doc": "31859186", "fecha": "22/02/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "774", "corregimiento": "Buitrera", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras leves y escalera artesanal afectada[cite: 71].",
        "personas": [
            {"nombre": "Mercedez Nelez Galvez", "doc": "14976409", "fecha": "03/07/1955", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jose Antonio Quiceno Posada", "doc": "29992989", "fecha": "15/12/1992", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "775", "corregimiento": "Dapa Podadero", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras mínimas que no representan riesgo en la infraestructura.",
        "personas": [
            {"nombre": "Hammer Ortiz Moreno", "doc": "1151934682", "fecha": "15/02/1991", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Paola Paz", "doc": "1085300884", "fecha": "24/03/1990", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Maria Paula Ortiz Paz", "doc": "1109939387", "fecha": "23/12/2021", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Aide Moreno Moreno", "doc": "31475217", "fecha": "20/09/1971", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "776", "corregimiento": "Dapa Rodadero", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda sin averías importantes que expongan el bienestar.",
        "personas": [
            {"nombre": "Cecilia Ortiz de Moreno", "doc": "29975201", "fecha": "11/12/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Jimena Moreno", "doc": "31482810", "fecha": "22/07/1978", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Jose Fernando Moreno", "doc": "16487873", "fecha": "01/01/1970", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Sebastian Moreno", "doc": "1006536626", "fecha": "13/02/2001", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "777", "corregimiento": "Dapa Rodadero", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado sin daños estructurales de gravedad.",
        "personas": [
            {"nombre": "Graciela Ortiz Urbano", "doc": "31477512", "fecha": "24/03/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alexandra Gomez Ortiz", "doc": "1118289649", "fecha": "07/07/1988", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Valery Muñoz Gomez", "doc": "1109191885", "fecha": "03/06/2010", "es_jefe": False, "sexo": "F", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "778", "corregimiento": "Buitrera", "prioridad": "BAJA",
        "observaciones_evaluador": "Innspección completada. Prioridad baja[cite: 71].",
        "personas": [
            {"nombre": "Hoover Lame Camoyo", "doc": "1007200987", "fecha": "23/03/1998", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Daysi Paola Tombe", "doc": "1064428646", "fecha": "27/01/2006", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "779", "corregimiento": "Montañitas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras superficiales en mampostería.",
        "personas": [
            {"nombre": "Paula Andrea Martinez Muñoz", "doc": "1120504564", "fecha": "22/07/1994", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hanser Madain Mesa", "doc": "1118310482", "fecha": "28/12/1998", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "780", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Muros con fisuras horizontales por desplazamiento.",
        "personas": [
            {"nombre": "Maria Helena", "doc": "31960013", "fecha": "18/02/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "781", "corregimiento": "Montañitas", "prioridad": "BAJA",
        "observaciones_evaluador": "Averías menores en mampostería y tejas de fibrocemento caídas por falta de amarre.",
        "personas": [
            {"nombre": "Ricaute Noguera", "doc": "6340828", "fecha": "21/01/1957", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 761-781...")
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
        print(f"MIGRACIÓN LOTE 761-781 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
