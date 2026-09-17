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
        "num_formulario": "1614", "corregimiento": "Guacandá", "prioridad": "BAJA",
        "observaciones_evaluador": "Esperanza Bonilla Pachane - Hogar Voces Melosas, prioridad baja (RUFE-1614).",
        "personas": [{"nombre": "Esperanza Bonilla Pachane", "doc": "29582105", "fecha": "03/02/1972", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1615", "corregimiento": "Guacandá", "prioridad": "BAJA",
        "observaciones_evaluador": "Patricia Agudela Castillo - Hogar Las Pingüinas, prioridad baja (RUFE-1615).",
        "personas": [{"nombre": "Patricia Agudela Castillo", "doc": "66846114", "fecha": "14/10/1968", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1616", "corregimiento": "Nueva Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Ana Ceng Santa Cruz Burbano - Hogar Vanacar, prioridad baja (RUFE-1616).",
        "personas": [{"nombre": "Ana Ceng Santa Cruz Burbano", "doc": "1118303704", "fecha": "09/06/1995", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1617", "corregimiento": "Estrella", "prioridad": "BAJA",
        "observaciones_evaluador": "Oto Saming Nicos - La Hamiquita Roo9, prioridad baja (RUFE-1617).",
        "personas": [{"nombre": "Oto Saming Nicos", "doc": "31481968", "fecha": "25/09/1979", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1618", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Sandra Margarita Guzman - Mas Amigos, prioridad baja (RUFE-1618).",
        "personas": [{"nombre": "Sandra Margarita Guzman", "doc": "66769280", "fecha": "29/07/1973", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1619", "corregimiento": "La Estancia", "prioridad": "BAJA",
        "observaciones_evaluador": "Luz Viviana Henao Grande - Pequeñas Personitas, prioridad baja (RUFE-1619).",
        "personas": [{"nombre": "Luz Viviana Henao Grande", "doc": "67040316", "fecha": "03/09/1985", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1620", "corregimiento": "Bellavista", "prioridad": "BAJA",
        "observaciones_evaluador": "Lucia Echavarria Orejuela - Los Juanitos, prioridad baja (RUFE-1620).",
        "personas": [{"nombre": "Lucia Echavarria Orejuela", "doc": "31473531", "fecha": "22/03/1969", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1621", "corregimiento": "Bellavista", "prioridad": "BAJA",
        "observaciones_evaluador": "Luz Dary Cruz Alba - Mi Chocita, prioridad baja (RUFE-1621).",
        "personas": [{"nombre": "Luz Dary Cruz Alba", "doc": "31467312", "fecha": "06/09/1956", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1622", "corregimiento": "Bellavista", "prioridad": "BAJA",
        "observaciones_evaluador": "Hilary Vanesa Londoño - Prioridad baja (RUFE-1622).",
        "personas": [{"nombre": "Hilary Vanesa Londoño", "doc": "1116372001", "fecha": "23/01/2004", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1623", "corregimiento": "Yumbo", "prioridad": "BAJA",
        "observaciones_evaluador": "Rosa Maria Acosta Gomez - Hogar Traviesos, prioridad baja (RUFE-1623).",
        "personas": [{"nombre": "Rosa Maria Acosta Gomez", "doc": "31486271", "fecha": "11/09/1982", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1624", "corregimiento": "Madrigal", "prioridad": "BAJA",
        "observaciones_evaluador": "Davy Espinosa Beltran - Los Saltamontes, prioridad baja (RUFE-1624).",
        "personas": [{"nombre": "Davy Espinosa Beltran", "doc": "31472745", "fecha": "01/11/1966", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1625", "corregimiento": "Madrigal", "prioridad": "BAJA",
        "observaciones_evaluador": "Delaly Cuenca Cruz - Los Paticos, prioridad baja (RUFE-1625).",
        "personas": [{"nombre": "Delaly Cuenca Cruz", "doc": "66778620", "fecha": "02/03/1976", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1626", "corregimiento": "Madrigal", "prioridad": "BAJA",
        "observaciones_evaluador": "Sandra Solay Trochas Transito - Ratoncitos, prioridad baja (RUFE-1626).",
        "personas": [{"nombre": "Sandra Solay Trochas Transito", "doc": "31482110", "fecha": "24/09/1979", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1627", "corregimiento": "Pandigoso", "prioridad": "BAJA",
        "observaciones_evaluador": "Juana Emilia Trochez - Hogar Michin, sin afectaciones visibles (RUFE-1627).",
        "personas": [{"nombre": "Juana Emilia Trochez", "doc": "25395749", "fecha": "05/02/1973", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1628", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Viviana Hilamo - Mi primera compañía, sin afectaciones visibles (RUFE-1628).",
        "personas": [{"nombre": "Viviana Hilamo", "doc": "1118286944", "fecha": "21/06/1987", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1629", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Lucila Murillo y Jorge Mosquera - Prioridad baja (RUFE-1629).",
        "personas": [
            {"nombre": "Lucila Murillo", "doc": "31395685", "fecha": "07/02/1964", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Jorge Mosquera", "doc": "16470980", "fecha": "21/04/1958", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1630", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Abraham Clavijo y Onice Belandia - Desprendimiento de pañete y fisuras mínimas (RUFE-1630).",
        "personas": [
            {"nombre": "Abraham Clavijo", "doc": "19425969", "fecha": "16/12/1960", "es_jefe": True, "sexo": "M", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Onice Belandia", "doc": "52119927", "fecha": "01/01/1970", "es_jefe": False, "sexo": "F", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Franklin Stliven Clavijo Belandia", "doc": "1111479883", "fecha": "26/10/2006", "es_jefe": False, "sexo": "M", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1631", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Irma Cartagena - Fisura en la junta de muro (RUFE-1631).",
        "personas": [
            {"nombre": "Irma Cartagena", "doc": "24572879", "fecha": "20/05/1955", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Mari Luz Mejia", "doc": "31497164", "fecha": "06/09/1982", "es_jefe": False, "sexo": "F", "parentesco": "Familiar", "etnia": "Ninguna"},
            {"nombre": "Lauren Acevedo", "doc": "1107066409", "fecha": "14/07/2009", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"}
        ]
    },
    {
        "num_formulario": "1632", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Clara Ines Mosquera Murillo - Grietas en muros ya arregladas (RUFE-1632).",
        "personas": [{"nombre": "Clara Ines Mosquera Murillo", "doc": "31324741", "fecha": "23/09/1983", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"}]
    },
    {
        "num_formulario": "1633", "corregimiento": "Panorama", "prioridad": "BAJA",
        "observaciones_evaluador": "Esther Osorio y Carlos Alirio Ayala - Fisuras del pañete del cielo raso (RUFE-1633).",
        "personas": [
            {"nombre": "Esther Osorio", "doc": "66715746", "fecha": "25/04/1970", "es_jefe": True, "sexo": "F", "parentesco": "Jefe de Hogar", "etnia": "Ninguna"},
            {"nombre": "Carlos Alirio Ayala", "doc": "102761217", "fecha": "15/01/1964", "es_jefe": False, "sexo": "M", "parentesco": "Pareja", "etnia": "Ninguna"},
            {"nombre": "Erika Jhoana Vergara", "doc": "1118296242", "fecha": "12/07/1991", "es_jefe": False, "sexo": "F", "parentesco": "Hijo(a)", "etnia": "Ninguna"},
            {"nombre": "Samuel Bastidas", "doc": "1111486400", "fecha": "31/12/1942", "es_jefe": False, "sexo": "M", "parentesco": "Familiar", "etnia": "Ninguna"},
            {"nombre": "Maria Leila Rojas", "doc": "29769987", "fecha": "01/01/1970", "es_jefe": False, "sexo": "F", "parentesco": "Familiar", "etnia": "Ninguna"}
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
    print("Iniciando ENRIQUECIMIENTO FINAL Lote 1614-1633...")
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
                
                cur.execute("SELECT id FROM public.rufe_personas WHERE documento_identidad = %s", (p["doc"],))
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
        print(f"MIGRACIÓN LOTE 1614-1633 EXITOSA.")
        print(f"Formularios -> Creados: {formularios_creados} | Actualizados: {formularios_actualizados}")
        print(f"Personas    -> Insertadas: {personas_creadas} | Actualizadas: {personas_actualizadas}")
        print(f"==================================================")
        
    except Exception as e:
        print(f"Error en BD: {e}")
    finally:
        if 'conn' in locals(): cur.close(); conn.close()

if __name__ == "__main__":
    main()
