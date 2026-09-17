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

# Consolidado de RUFEs desde el 385 hasta el 416
LOTES_NUEVOS_RUFE = [
    # --- LOTE FALTANTE (385-410) ---
    {
        "num_formulario": "385", "corregimiento": "Mulalo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Escaleras, grietas y afectaciones en la estructura. Muros de mamposteria con fisuras.",
        "personas": [
            {"nombre": "Dovinson Castrillon", "doc": "16930258", "fecha": "11/10/1980", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nancy Otero", "doc": "21232794052", "fecha": "15/01/1987", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "386", "corregimiento": "Mulalo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Desprendimiento de revoque y enchape. Desplome de muro en habitación. Se recomienda tumbar muro.",
        "personas": [
            {"nombre": "Carmen Grisales", "doc": "66915809", "fecha": "07/01/1959", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "389", "corregimiento": "Mulalo", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda construida en material con tejas movidas, grietas leves en muros.",
        "personas": [
            {"nombre": "Flor Alba Rosero", "doc": "29939430", "fecha": "15/01/1965", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "395", "corregimiento": "Guacanda", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda Bifamiliar. Teja de zinc en pésimo estado. Cede la estructura.",
        "personas": [
            {"nombre": "Rosa Ana Gonzalez Bonilla", "doc": "34372918", "fecha": "22/11/1966", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Maria Virginia Gonzalez Castillo", "doc": "1002946779", "fecha": "21/08/2001", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "396", "corregimiento": "Guacanda", "prioridad": "BAJA",
        "observaciones_evaluador": "Fisuras superficiales en diferentes muros. Desplazamiento leve de muro de la cocina.",
        "personas": [
            {"nombre": "Edinson Guapacha", "doc": "6423451", "fecha": "22/04/1969", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "400", "corregimiento": "Dapa", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda no habitable.",
        "personas": [
            {"nombre": "Raquel Garcia", "doc": "25262411", "fecha": "21/08/1940", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Nilson Quilindo", "doc": "1118292669", "fecha": "13/06/1993", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "404", "corregimiento": "Guacanda", "prioridad": "BAJA",
        "observaciones_evaluador": "Vivienda construida en material con daños menores. Pared posterior caída por el sismo.",
        "personas": [
            {"nombre": "Luciano Florez", "doc": "5371730", "fecha": "09/01/1943", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Eucaris Cataño Loaiza", "doc": "31234463", "fecha": "30/11/1949", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "407", "corregimiento": "Mulalo", "prioridad": "MEDIA",
        "observaciones_evaluador": "Vivienda en bahareque y material con la parte de bahareque colapsada.",
        "personas": [
            {"nombre": "Aracely Garcia", "doc": "29940357", "fecha": "11/01/1973", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "410", "corregimiento": "El Pedregal", "prioridad": "ALTA",
        "observaciones_evaluador": "Antepecho de la losa del 2do piso suelto, amenaza con caer a la calle. Peligro para los peatones. Demolición controlada urgente.",
        "personas": [
            {"nombre": "Jose Domingo Lozano", "doc": "6549465", "fecha": "29/07/1940", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    
    # --- LOTE 411-416 ---
    {
        "num_formulario": "411", "corregimiento": "Nuevo Horizonte", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda en bahareque fuertemente agrietada, se recomienda desalojo por peligro inminente de caída.",
        "personas": [
            {"nombre": "Cesar Mondragon", "doc": "1118288534", "fecha": "31/05/1991", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "413", "corregimiento": "Buenos Aires", "prioridad": "ALTA",
        "observaciones_evaluador": "Vivienda sin vigas de amarre. Muros sueltos. Techo y remates de columnas colapsados.",
        "personas": [
            {"nombre": "Jhon Jairo Ipiales", "doc": "16462204", "fecha": "21/03/1982", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "415", "corregimiento": "Nuevo Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Muro suelto en fachada de 2do piso por falta de columnas. Suelta baranda 2 piso.",
        "personas": [
            {"nombre": "Karina Paredes", "doc": "31580778", "fecha": "05/10/1979", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "416", "corregimiento": "Nuevo Horizonte", "prioridad": "MEDIA",
        "observaciones_evaluador": "Losa apoyada en bahareque y madera. Se recomienda demoler losa por peso.",
        "personas": [
            {"nombre": "Ana Maria Henao", "doc": "31144118", "fecha": "26/01/1952", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}
        ]
    }
]

def calcular_edad_2026(fecha_str):
    match = re.search(r'(19\d{2}|20\d{2})', str(fecha_str))
    if match:
        return 2026 - int(match.group(1))
    return None

def main():
    print("Iniciando ENRIQUECIMIENTO (Upsert) Lote 385-416 con validación de Foreign Key...")
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = True
        cur = conn.cursor()
        
        formularios_creados, formularios_actualizados = 0, 0
        personas_creadas, personas_actualizadas = 0, 0
        
        # 1. OBTENER UN REPORTE MAESTRO VÁLIDO
        cur.execute("SELECT id FROM public.reportes_comunitarios LIMIT 1;")
        res_reporte = cur.fetchone()
        
        if not res_reporte:
            # Si por alguna razón la tabla está vacía, creamos uno de emergencia
            reporte_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO public.reportes_comunitarios (id, activo) 
                VALUES (%s, true) ON CONFLICT DO NOTHING;
            """, (reporte_id,))
        else:
            reporte_id = res_reporte[0]
            
        print(f"[*] Usando Reporte Maestro ID: {reporte_id} para cumplir Foreign Key.")
        
        for form in LOTES_NUEVOS_RUFE:
            num_limpio = form["num_formulario"].lstrip('0')
            
            cur.execute("SELECT id FROM public.rufe_formularios WHERE numero_formulario = %s", (num_limpio,))
            resultado = cur.fetchone()
            
            if resultado:
                form_id = resultado[0]
                cur.execute("""
                    UPDATE public.rufe_formularios 
                    SET prioridad = %s, observaciones_evaluador = %s
                    WHERE id = %s;
                """, (form["prioridad"], form["observaciones_evaluador"], form_id))
                formularios_actualizados += 1
            else:
                # INSERCIÓN CON EL REPORTE_ID VÁLIDO
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
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE REPLACE(documento_identidad, '.', '') = %s", (p["doc"],))
                res_persona = cur.fetchone()
                
                if res_persona:
                    persona_id = res_persona[0]
                    cur.execute("""
                        UPDATE public.rufe_personas 
                        SET fecha_nacimiento = %s, edad = %s, es_jefe_hogar = %s, parentesco = %s, sexo = %s, etnia = %s
                        WHERE id = %s;
                    """, (p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"], persona_id))
                    personas_actualizadas += 1
                else:
                    cur.execute("""
                        INSERT INTO public.rufe_personas 
                        (rufe_formulario_id, nombre_completo, documento_identidad, fecha_nacimiento, edad, es_jefe_hogar, parentesco, sexo, etnia)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (form_id, p["nombre"], p["doc"], p["fecha"], edad_calc, p["es_jefe"], p["parentesco"], p["sexo"], p["etnia"]))
                    personas_creadas += 1

        print(f"\n==================================================")
        print(f"MIGRACIÓN LOTE 385-416 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
