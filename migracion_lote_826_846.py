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
        "num_formulario": "826", "corregimiento": "Terrazas de Rivera", "prioridad": "MEDIA",
        "observaciones_evaluador": "Asentamiento de piso construido sobre relleno mal compactado e inminente riesgo de afectación estructural[cite: 64].",
        "personas": [
            {"nombre": "María de Pilar Ceballos", "doc": "66859941", "fecha": "04/01/1973", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Belarmina Izquierda", "doc": "31268663", "fecha": "13/05/1955", "es_jefe": False, "sexo": "F", "parentesco": "Madre", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "827", "corregimiento": "Riveras de Yumbo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda evaluada con prioridad media[cite: 64].",
        "personas": [
            {"nombre": "Rosa Antonia Martinez", "doc": "31951798", "fecha": "14/06/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "828", "corregimiento": "Riveras de Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda en material con fisuras superficiales menores en mampostería[cite: 64].",
        "personas": [
            {"nombre": "Luz Betty Gonzalez", "doc": "25061186", "fecha": "10/05/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Arturo Medina", "doc": "310253590", "fecha": "27/08/1961", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Tanny Arosta", "doc": "25053440", "fecha": "01/01/1975", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "829", "corregimiento": "Riveras de Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Inspección completada sin novedades estructurales mayores.",
        "personas": [
            {"nombre": "Fernanda Yela Ramirez", "doc": "1118290197", "fecha": "30/01/1988", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Pablo Ceballos", "doc": "97481045", "fecha": "26/08/1983", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Saray Sofia Ceballos", "doc": "1109196408", "fecha": "17/08/2016", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "830", "corregimiento": "Riveras de Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con acabados menores revisados.",
        "personas": [
            {"nombre": "Maria Astrid Yepes", "doc": "51706060", "fecha": "15/04/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hermes Charria", "doc": "16354390", "fecha": "03/08/1959", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Daniel Charria", "doc": "0", "fecha": "01/01/1990", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "831", "corregimiento": "Riveras de Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Muros con fisuras superficiales, estructura estable[cite: 65].",
        "personas": [
            {"nombre": "Aura Maria Bedoya Mejia", "doc": "31485512", "fecha": "04/01/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Rodrigo Pizarro", "doc": "94457862", "fecha": "03/09/1975", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Sara Pizarro", "doc": "1116373659", "fecha": "22/04/2007", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "832", "corregimiento": "Riveras de Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda verificada sin riesgo estructural crítico[cite: 65].",
        "personas": [
            {"nombre": "Janeth Ramirez", "doc": "66903896", "fecha": "16/03/1974", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Alvaro Mesía", "doc": "1118304984", "fecha": "14/08/1995", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Adeline Mesía", "doc": "1232813400", "fecha": "10/08/2020", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "833", "corregimiento": "Condado", "prioridad": "ALTA",
        "observaciones_evaluador": "Inmueble evaluado con afectaciones severas en elementos de soporte[cite: 65].",
        "personas": [
            {"nombre": "Alonso Lopez Chilito", "doc": "16445637", "fecha": "06/01/1954", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "834", "corregimiento": "Belalcazar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con riesgo medio de afectación en mampostería[cite: 65].",
        "personas": [
            {"nombre": "Maria Yolanda Salcedo", "doc": "29972256", "fecha": "30/06/1950", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Mariana Silva Montero", "doc": "1027807866", "fecha": "02/07/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Catalina Silva Montero", "doc": "31481489", "fecha": "28/03/1979", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "835", "corregimiento": "Uribe", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda unifamiliar con revisión completada[cite: 65].",
        "personas": [
            {"nombre": "Helen Marmolejo", "doc": "1118296813", "fecha": "17/09/1991", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "836", "corregimiento": "Ciudad Guabinas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble verificado con prioridad baja[cite: 65].",
        "personas": [
            {"nombre": "Luz Adriana Vasquez Vivas", "doc": "1118286426", "fecha": "12/02/1987", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Julian Andres Villalobos Perea", "doc": "1118306738", "fecha": "10/03/1996", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Samuel Villalobos Vasquez", "doc": "11232834349", "fecha": "02/10/2024", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "837", "corregimiento": "Sector Varios", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con fisuras en muros divisorios[cite: 66].",
        "personas": [
            {"nombre": "Zora Angulo Mercado", "doc": "7059042925", "fecha": "10/12/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Deiris Paola Mercado", "doc": "33272218", "fecha": "09/07/1980", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "838", "corregimiento": "Sector Varios", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras menores y acabados revisados[cite: 66].",
        "personas": [
            {"nombre": "Jorge Enrique Grijalba", "doc": "1112795570", "fecha": "14/02/1994", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Andry Alejandra Londoño", "doc": "16460212", "fecha": "23/06/1980", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Hillary Alexandra Londoño", "doc": "123282", "fecha": "23/09/2016", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Joshua Acdihel Grijalba Londoño", "doc": "1109197515", "fecha": "13/05/2014", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "839", "corregimiento": "Sector Varios", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con prioridad baja verificado[cite: 66].",
        "personas": [
            {"nombre": "Carlos Alberto Loaiza", "doc": "6531682", "fecha": "15/12/1968", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maribel Vargas Lopez", "doc": "66862978", "fecha": "22/02/1973", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "840", "corregimiento": "Cas Americas", "prioridad": "ALTA",
        "observaciones_evaluador": "Hogar con presencia de animales domésticos y afectación grave en mampostería[cite: 66].",
        "personas": [
            {"nombre": "Nesenia Vasquez", "doc": "1118292637", "fecha": "24/10/1989", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Yisel Rojas Vasquez", "doc": "1109679382", "fecha": "14/01/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Mariana Milagros Bernal Vasquez", "doc": "1101211183", "fecha": "02/05/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Rivera", "doc": "1309884", "fecha": "17/06/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "841", "corregimiento": "Las Américas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con afectación menor en mampostería[cite: 67].",
        "personas": [
            {"nombre": "Jhonatan Perez", "doc": "3118284684", "fecha": "21/09/1986", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Perez Buitrago", "doc": "31486993", "fecha": "19/10/1988", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Dayana Buitrago", "doc": "3116866678", "fecha": "13/01/2001", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Delby Buitrago", "doc": "3157841537", "fecha": "31/10/2004", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "842", "corregimiento": "Las Américas", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras menores en mampostería[cite: 67].",
        "personas": [
            {"nombre": "Amparo Vasquez", "doc": "31469183", "fecha": "28/05/1958", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Karen Julieth Vasquez", "doc": "1118282997", "fecha": "12/02/2003", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Dominic Soto", "doc": "1116384829", "fecha": "30/07/2023", "es_jefe": False, "sexo": "M", "parentesco": "Nieto(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "843", "corregimiento": "Las Américas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inspección de mampostería completada sin novedades críticas[cite: 67].",
        "personas": [
            {"nombre": "Ingrid Noguera Betancourth", "doc": "3118285296", "fecha": "12/12/1986", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jhan Carlos Betancourth", "doc": "0", "fecha": "01/01/1990", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Ociana Betancourth", "doc": "0", "fecha": "01/01/1995", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "844", "corregimiento": "Las Américas", "prioridad": "BAJA",
        "observaciones_evaluador": "Inmueble con prioridad baja verificado[cite: 67].",
        "personas": [
            {"nombre": "Andres Felipe Espitia", "doc": "7726444093", "fecha": "12/12/1954", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juliett Daniela Torres Espitia", "doc": "7032429256", "fecha": "18/05/1989", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Ian Andres Espitia Torres", "doc": "1116380304", "fecha": "13/07/2016", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Aaron Daniel Espitia Torres", "doc": "1116382929", "fecha": "20/07/2020", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "845", "corregimiento": "Las Américas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda con daños estructurales significativos en muros de contención e internos[cite: 67].",
        "personas": [
            {"nombre": "Mersner Elizabeth Urueña Mora", "doc": "29218959", "fecha": "20/09/1984", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Moises Ponce", "doc": "16458889", "fecha": "23/10/1979", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "846", "corregimiento": "Las Américas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Inmueble con fisuras en muros y acabados reportados[cite: 67].",
        "personas": [
            {"nombre": "Diana Alexandra Moreno Vargas", "doc": "419417772", "fecha": "28/08/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 826-846...")
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
        print(f"MIGRACIÓN LOTE 826-846 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
