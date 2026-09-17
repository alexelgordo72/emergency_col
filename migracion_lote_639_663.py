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
        "num_formulario": "639", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda rural en bahareque muy antigua y deteriorada, fuertemente afectada por el sismo con fisuras en muros y techos[cite: 59].",
        "personas": [
            {"nombre": "Aldemar Mosquera", "doc": "6096095", "fecha": "14/01/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Elizabeth Mosquera", "doc": "31469426", "fecha": "05/03/1971", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "640", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Muro lateral muy inestable; se desprendió el techo de la bodega y se inclinó un piso prefabricado. Orden de demolición inmediata.",
        "personas": [
            {"nombre": "Amanda Martinez", "doc": "31859186", "fecha": "22/02/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "641", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda rural de 1 piso en bahareque en muy mal estado, con muro colapsado y requerimiento de reconstrucción en ladrillo.",
        "personas": [
            {"nombre": "Teobaldo Collazos", "doc": "14576614", "fecha": "25/09/1972", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jackeline Barreto", "doc": "29581649", "fecha": "28/08/1967", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "642", "corregimiento": "Campestre Real", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda de material con fisuras leves en mampostería y en repello de muros.",
        "personas": [
            {"nombre": "Luis Alfonso Lopez", "doc": "16340139", "fecha": "13/12/1956", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Celia Morales de Lopez", "doc": "38710034", "fecha": "29/07/1960", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "643", "corregimiento": "L勒eras", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras en la parte interna de la placa y desprendimiento de revestimiento en el baño[cite: 61].",
        "personas": [
            {"nombre": "Doris Bolaños", "doc": "31473010", "fecha": "01/06/1987", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jose Libardo Prado", "doc": "6493917", "fecha": "01/01/1970", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Maria Jose Motato Riascos", "doc": "1116379226", "fecha": "01/01/2010", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Zamara Motato Riascos", "doc": "0", "fecha": "01/01/2012", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "644", "corregimiento": "Campestre Real", "prioridad": "ALTA",
        "observaciones_evaluador": "Alerta por colapso inminente de vivienda vecina que afecta el costado norte[cite: 61].",
        "personas": [
            {"nombre": "Ilian Darlyn Hincapie", "doc": "229404016", "fecha": "01/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "645", "corregimiento": "Campestre Real", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda con fisuras en muros y desprendimiento de repellos en juntas de construcción y placa superior[cite: 61].",
        "personas": [
            {"nombre": "Diana Laura Camila Escobar Rivera", "doc": "1144704246", "fecha": "21/06/1997", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "646", "corregimiento": "Campestre Real", "prioridad": "ALTA",
        "observaciones_evaluador": "Muros sin sistema de confinamiento con puntos de apoyo deficientes. Riesgo alto de colapso de cubierta[cite: 60].",
        "personas": [
            {"nombre": "Danissa Sarmiento", "doc": "31484309", "fecha": "01/01/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Cielo Bolaños", "doc": "31462204", "fecha": "02/03/1998", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "647", "corregimiento": "Dionisio", "prioridad": "MEDIA",
        "observaciones_evaluador": "Separación entre viga aérea y columna, con pérdida de concreto en parte inferior y riesgo de volcamiento en muro de fachada[cite: 62].",
        "personas": [
            {"nombre": "Gissela Velez Gonzalez", "doc": "1118297326", "fecha": "19/08/2015", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "648", "corregimiento": "Bolivar", "prioridad": "MEDIA",
        "observaciones_evaluador": "Columna con grieta considerable; requiere revisión de ingeniero de infraestructura[cite: 62].",
        "personas": [
            {"nombre": "Nilson Puente", "doc": "16462336", "fecha": "14/08/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "649", "corregimiento": "Bolivar", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras horizontales y verticales por separación de elementos; estuco desprendido en cielo raso y muros de habitaciones[cite: 62].",
        "personas": [
            {"nombre": "Gilberto Valencia", "doc": "16283863", "fecha": "28/08/1934", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "650", "corregimiento": "Bolivar", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales y dilatación en muros y vigas[cite: 60].",
        "personas": [
            {"nombre": "Jennifer Valdivieso", "doc": "1118260271", "fecha": "26/02/1999", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "651", "corregimiento": "Comfandi", "prioridad": "ALTA",
        "observaciones_evaluador": "Muros perimetrales e internos con alto riesgo de colapso, mampostería comprometida en un 80% sin estructura de confinamiento[cite: 61].",
        "personas": [
            {"nombre": "Maria Elena Quijano Sanchez", "doc": "31465329", "fecha": "11/02/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "652", "corregimiento": "Comfandi", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en muros, escaleras y cielo raso[cite: 61].",
        "personas": [
            {"nombre": "Cora Marina Hernandez", "doc": "31469359", "fecha": "10/02/1962", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Sandra Mendoza", "doc": "29974160", "fecha": "01/01/1970", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "653", "corregimiento": "Belalcazar", "prioridad": "ALTA",
        "observaciones_evaluador": "Cuchilla de tercer piso descolgada y sujeta únicamente de listones y cubierta; alto riesgo de colapso con recomendación de demolición o desmonte[cite: 63].",
        "personas": [
            {"nombre": "Gloria Yolima Fernandez", "doc": "16690490", "fecha": "08/04/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Pablo Gomez Mendez", "doc": "16844405", "fecha": "02/01/1960", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "654", "corregimiento": "Las Vegas", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en material con muro perimetral descolgado por grietas en juntas.",
        "personas": [
            {"nombre": "Martha Lucia", "doc": "29581281", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "655", "corregimiento": "Miravalle San Jose", "prioridad": "ALTA",
        "observaciones_evaluador": "Muros azotados gravemente, se recomienda demolición y evacuación[cite: 62].",
        "personas": [
            {"nombre": "Ximena Perez Mesa", "doc": "41925904", "fecha": "19/02/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Juan Pablo Mesa Nicholls", "doc": "14878210", "fecha": "07/04/1986", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "656", "corregimiento": "Alto Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con 90% sin riesgo, pero con reporte de muros apretados[cite: 62].",
        "personas": [
            {"nombre": "Gustavo Andres Gutierrez", "doc": "1118286579", "fecha": "10/05/1981", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luis Alberto Herrery", "doc": "164512719", "fecha": "26/10/1987", "es_jefe": False, "sexo": "M", "parentesco": "Otro", "etnia": "Ninguna"},
            {"nombre": "Maria Alexandra", "doc": "31134805", "fecha": "01/01/1990", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "657", "corregimiento": "El Condado", "prioridad": "ALTA",
        "observaciones_evaluador": "Destrucción total, habitantes desplazados[cite: 62].",
        "personas": [
            {"nombre": "Maria Fausta Ordoñez", "doc": "65550148", "fecha": "20/09/1963", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Augusto Ortiz Peralta", "doc": "1029043", "fecha": "31/01/1981", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "658", "corregimiento": "Dapa El Solitario", "prioridad": "ALTA",
        "observaciones_evaluador": "Muros, vigas y placa con grietas considerables; recomendación de no habitar por alto riesgo[cite: 62].",
        "personas": [
            {"nombre": "Martha Lucia Ortiz Benavidez", "doc": "1144075941", "fecha": "27/03/1951", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Hernan Alberto Ortiz Muñoz", "doc": "16445009", "fecha": "30/09/1906", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Blanca Gradys Benavidez Urbano", "doc": "29975259", "fecha": "01/01/1970", "es_jefe": False, "sexo": "F", "parentesco": "Otro", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "659", "corregimiento": "San Marcos", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en el suelo, caída de pared de ladrillo sin riesgo inmediato[cite: 63].",
        "personas": [
            {"nombre": "Abel Castro Martinez", "doc": "16435358", "fecha": "28/10/1965", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "661", "corregimiento": "Alto Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Daños en paredes, habitante madre cabeza de hogar[cite: 63].",
        "personas": [
            {"nombre": "Chicanbang", "doc": "1061692885", "fecha": "15/01/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "662", "corregimiento": "Miravalle El Chocho", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda sin daños aparentes estructurales, calificada sin peligro[cite: 63].",
        "personas": [
            {"nombre": "Leon Benavidez", "doc": "1412072", "fecha": "18/12/1996", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Luz Dary Benavidez", "doc": "331486927", "fecha": "26/06/1984", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "663", "corregimiento": "Buitrera", "prioridad": "BAJA",
        "observaciones_evaluador": "Muros afectados con grietas; columnas y vigas en buen estado sin riesgo latente[cite: 63].",
        "personas": [
            {"nombre": "Patricia Rojas", "doc": "31823689", "fecha": "19/02/1959", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jair Verde", "doc": "16622683", "fecha": "01/05/1962", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 639-663...")
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
        print(f"MIGRACIÓN LOTE 639-663 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
