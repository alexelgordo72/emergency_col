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
        "num_formulario": "551", "corregimiento": "Alto Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en acabados y paneles divisorios. Habitable.",
        "personas": [
            {"nombre": "Maria Elena Noronge Bellochi", "doc": "66839371", "fecha": "01/01/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "552", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en la losa, viga de madera en mal estado que soporta el entrepiso. Se requiere cambio.",
        "personas": [
            {"nombre": "Soac Ordonez Sonono", "doc": "0", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "553", "corregimiento": "Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en bahareque con afectaciones en muros y mampostería. Requiere refuerzo en viga de amarre.",
        "personas": [
            {"nombre": "Wilson Ortiz Buitrago", "doc": "316636538", "fecha": "08/08/1955", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "554", "corregimiento": "Miravalle Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Mampostería averiada sin sistema estructural y muros colapsados. Integrante adoptado con discapacidad (mudo-NN).",
        "personas": [
            {"nombre": "Angelita del Socorro Martinez", "doc": "66904296", "fecha": "19/05/1971", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "555", "corregimiento": "La Pica", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con fisuras mínimas en mampostería, techos corridos de la cubierta. Habitable.",
        "personas": [
            {"nombre": "Rosa Maria Herrera", "doc": "31469042", "fecha": "18/01/1963", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Elsa Nubia Imbachi", "doc": "29975350", "fecha": "04/12/1984", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "556", "corregimiento": "Buitrera Miravalle", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muros internos con desprendimiento de revestimiento y grietas horizontales.",
        "personas": [
            {"nombre": "Ana Maria Quinones Martinez", "doc": "68985788", "fecha": "02/12/1978", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "557", "corregimiento": "Buitrera", "prioridad": "ALTA",
        "observaciones_evaluador": "Mampostería comprometida, desprendimiento de muro en escaleras y grietas superficiales.",
        "personas": [
            {"nombre": "Abel Diaz", "doc": "16582846", "fecha": "29/01/1935", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "558", "corregimiento": "Miravalle", "prioridad": "ALTA",
        "observaciones_evaluador": "Muros sueltos y columna con desprendimiento de concreto y acero expuesto.",
        "personas": [
            {"nombre": "Jhonaton Santana", "doc": "1107042859", "fecha": "13/12/1987", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "559", "corregimiento": "San Marcos", "prioridad": "BAJA",
        "observaciones_evaluador": "Reparaciones locativas en mampostería y confinamiento para cuarto.",
        "personas": [
            {"nombre": "Mirlan Bernal", "doc": "51693523", "fecha": "10/02/1962", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "560", "corregimiento": "Montañitas", "prioridad": "ALTA",
        "observaciones_evaluador": "Estructura cedida, colapso de muros y desplome generalizado. Demolición total recomendada.",
        "personas": [
            {"nombre": "Maria Fernanda Perez Serna", "doc": "34561872", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "561", "corregimiento": "Dapa El Jardin", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda con desprendimiento de pañete y fisuras en muros divisorios.",
        "personas": [
            {"nombre": "Andrea Martinez", "doc": "118284572", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "562", "corregimiento": "Rincon Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Grietas verticales por separación de muros y desplazamiento del terreno. Riesgo de colapso inminente.",
        "personas": [
            {"nombre": "Maria Elena Segura", "doc": "681402815", "fecha": "01/01/1960", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "563", "corregimiento": "Alto Dapa", "prioridad": "MEDIA",
        "observaciones_evaluador": "Fisuras en muros y piso con hundimiento en la parte inferior.",
        "personas": [
            {"nombre": "Deysi Autado", "doc": "625422502", "fecha": "01/01/1980", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Liliana Siment", "doc": "66900476", "fecha": "01/01/1985", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "564", "corregimiento": "Miravalle", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en enchape y pintura.",
        "personas": [
            {"nombre": "Ferney de Jesus Guapacha", "doc": "10195179", "fecha": "14/08/1977", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "565", "corregimiento": "Miravalle", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en acabados de muros, no comprometidos.",
        "personas": [
            {"nombre": "Maria Alheno Campo", "doc": "6581402815", "fecha": "01/01/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "566", "corregimiento": "Alto Dapa Centro", "prioridad": "ALTA",
        "observaciones_evaluador": "Estructura con desplome, desprendimiento total de muros y techo de madera con inclinación. Demolición total recomendada.",
        "personas": [
            {"nombre": "Maria Fernanda Perez Serna", "doc": "34561872", "fecha": "01/01/1975", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "571", "corregimiento": "Alto Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Muro de contención de piedra con desprendimiento menor.",
        "personas": [
            {"nombre": "Noway", "doc": "16699273", "fecha": "01/01/1975", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "572", "corregimiento": "Alto Dapa", "prioridad": "BAJA",
        "observaciones_evaluador": "Cubierta totalmente deteriorada, sin columnas ni vigas, con inminente riesgo de colapso.",
        "personas": [
            {"nombre": "Jenni Paola Trujillo", "doc": "6114444092", "fecha": "01/01/1990", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO Lote 551-572...")
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
        print(f"MIGRACIÓN LOTE 551-572 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
